# ============================================================
# check.py - run a solution and compare it with the expected output
# ============================================================
# Language-neutral: it runs whatever command you give it after --
# and compares what that command prints. Standard library only.
#
#   py -3.13 check/check.py 01 -- python tasks/01_bookshelf/solution/main.py
#   py -3.13 check/check.py 04 -- java -cp out Main tasks/data
#   py -3.13 check/check.py 12 -- node tasks/12_library_api/solution/main.js tasks/data {port}
#
# Task ids: 01 to 12, B, and 12_stretch.
#   * 03 and 07 read their commands from data/input_03.txt and
#     data/input_07.txt; the checker pipes the file in for you.
#   * 11 runs your tests and checks every required test name
#     appears in the output and the run succeeds (exit code 0).
#   * 12 starts your server on a free port ({port} in the command
#     is replaced with it, or the port is added at the end), sends
#     the requests in check/api_script.json and compares the
#     responses. The server is stopped afterwards.
#
# Options (before the --):
#   --expected FILE   compare with this file instead
#   --timeout SECS    give up after this long (default 120)
#   --write           maintainers only: save the output as the
#                     expected file instead of comparing
#
# Exit code: 0 for PASS, 1 for FAIL, 2 for a usage problem.
# ============================================================

import http.client
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Pack layout: pack/check/check.py with pack/expected and pack/data.
# Repo layout: tasks/check/check.py (or tasks/check.py) with tasks/data.
ROOT = HERE.parent if HERE.name == "check" else HERE

STDIN_FILES = {"03": "input_03.txt", "07": "input_07.txt"}
TEST_TASKS = {"11"}
API_TASKS = {"12"}


# ------------------------------------------------------------
# Finding files
# ------------------------------------------------------------

def expected_path(task: str) -> Path:
    """expected/NN.txt (pack) or NN_name/expected.txt (repo)."""
    pack_file = ROOT / "expected" / f"{task}.txt"
    if pack_file.exists():
        return pack_file
    number, _, suffix = task.partition("_")
    name = f"expected_{suffix}.txt" if suffix else "expected.txt"
    for folder in sorted(ROOT.glob(f"{number}_*")):
        if (folder / name).exists():
            return folder / name
    return pack_file  # does not exist: reported by the caller


def child_env() -> dict[str, str]:
    """Ask every runtime we know about to print UTF-8 (the £ sign)."""
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    java = "-Dstdout.encoding=UTF-8 -Dstderr.encoding=UTF-8 -Dfile.encoding=UTF-8"
    env["JAVA_TOOL_OPTIONS"] = (env.get("JAVA_TOOL_OPTIONS", "") + " " + java).strip()
    env["DOTNET_CLI_UI_LANGUAGE"] = "en"
    return env


def resolve(command: list[str]) -> list[str]:
    """On Windows, find mvn.cmd, npm.cmd and friends from a bare name."""
    found = shutil.which(command[0])
    return [found, *command[1:]] if found else command


# ------------------------------------------------------------
# Comparing text
# ------------------------------------------------------------

def normalise(text: str) -> list[str]:
    """Line endings, trailing spaces and trailing blank lines never count."""
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def compare(expected: list[str], actual: list[str]) -> bool:
    for number, (want, got) in enumerate(zip(expected, actual), start=1):
        if want != got:
            print(f"FAIL: line {number} differs")
            print(f"  expected: {want}")
            print(f"  actual:   {got}")
            return False
    if len(actual) < len(expected):
        print(f"FAIL: output stops after {len(actual)} lines; expected {len(expected)}")
        print(f"  first missing line {len(actual) + 1}: {expected[len(actual)]}")
        return False
    if len(actual) > len(expected):
        print(f"FAIL: {len(actual) - len(expected)} extra lines after line {len(expected)}")
        print(f"  first extra line {len(expected) + 1}: {actual[len(expected)]}")
        return False
    print(f"PASS ({len(expected)} lines match)")
    return True


def decode(raw: bytes) -> str | None:
    """Strict UTF-8; a leading byte order mark (C# sometimes adds one) is dropped."""
    try:
        return raw.decode("utf-8").removeprefix("\ufeff")
    except UnicodeDecodeError:
        return None


# ------------------------------------------------------------
# Mode 1: plain stdout
# ------------------------------------------------------------

def run_plain(task: str, command: list[str], timeout: float) -> tuple[str | None, int]:
    stdin_name = STDIN_FILES.get(task)
    stdin = (ROOT / "data" / stdin_name).open("rb") if stdin_name else subprocess.DEVNULL
    try:
        done = subprocess.run(resolve(command), stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=timeout, env=child_env())
    finally:
        if stdin_name:
            stdin.close()  # type: ignore[union-attr]
    text = decode(done.stdout)
    if done.returncode != 0:
        print(f"note: the program exited with code {done.returncode}")
        err = done.stderr.decode("utf-8", errors="replace").strip()
        if err:
            print("  last lines of stderr:")
            for line in err.splitlines()[-5:]:
                print(f"    {line}")
    return text, done.returncode


# ------------------------------------------------------------
# Mode 2: unit tests (task 11)
# ------------------------------------------------------------

def squash(text: str) -> str:
    """test_borrow_reduces_available, borrowReducesAvailable and
    BorrowReducesAvailable all squash to borrowreducesavailable."""
    text = re.sub(r"[^a-z0-9]", "", text.lower())
    return text


def required_tests(path: Path) -> list[str]:
    return [line.split()[0] for line in normalise(path.read_text(encoding="utf-8")) if line.strip()]


def run_tests(command: list[str], timeout: float) -> tuple[str, int]:
    done = subprocess.run(resolve(command), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=timeout, env=child_env())
    return done.stdout.decode("utf-8", errors="replace"), done.returncode


def check_tests(names: list[str], output: str) -> list[str]:
    """'name PASS' for each required test that appears in the output
    of a successful run, 'name MISSING' for one that does not."""
    squashed = squash(output)
    lines = []
    for name in names:
        key = squash(name)
        key = key[4:] if key.startswith("test") else key  # testBorrow... or borrow...
        lines.append(f"{name} {'PASS' if key in squashed else 'MISSING'}")
    return lines


# ------------------------------------------------------------
# Mode 3: a running API (task 12)
# ------------------------------------------------------------

SERVER_HOST = "127.0.0.1"


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_for_port(port: int, process: subprocess.Popen[bytes], timeout: float) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            return False
        # Servers differ: some listen on IPv4 (127.0.0.1), some on IPv6 (::1),
        # e.g. Node binds "localhost" to ::1. Find the one that answers once,
        # then use it for every request (trying "localhost" each time is slow
        # on Windows, which tries IPv6 first).
        for host in ("127.0.0.1", "::1"):
            try:
                with socket.create_connection((host, port), timeout=1):
                    global SERVER_HOST
                    SERVER_HOST = host
                    return True
            except OSError:
                pass
        time.sleep(0.2)
    return False


def stop(process: subprocess.Popen[bytes]) -> None:
    """Stop the server and anything it started (mvn, dotnet and npm
    run the real program as a child process). Only this tree."""
    if process.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(process.pid)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        os.killpg(process.pid, signal.SIGTERM)
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()


def canonical(value: object) -> str:
    """Key order and spacing never count: sorted keys, no spaces."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def transcript(port: int) -> list[str]:
    script = json.loads((HERE / "api_script.json").read_text(encoding="utf-8"))
    lines: list[str] = []
    for step in script:
        conn = http.client.HTTPConnection(SERVER_HOST, port, timeout=10)
        body = step.get("body")
        headers = {"Content-Type": "application/json"} if body is not None else {}
        conn.request(step["method"], step["path"], body=body.encode("utf-8") if body is not None else None,
                     headers=headers)
        response = conn.getresponse()
        raw = response.read()
        conn.close()
        kind = response.getheader("Content-Type", "none")
        kind = "json" if kind.split(";")[0].strip().lower() == "application/json" else kind
        shown = f" {body}" if body is not None else ""
        lines.append(f"{step['method']} {step['path']}{shown}")
        lines.append(f"{response.status} {kind}")
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            lines.append(f"not JSON: {raw[:80]!r}")
            continue
        if isinstance(value, list):
            if not value:
                lines.append("[]")
            else:
                lines.append("[")
                lines.extend(f"  {canonical(item)}" for item in value)
                lines.append("]")
        else:
            lines.append(canonical(value))
    return lines


def run_api(command: list[str], timeout: float) -> list[str] | None:
    port = free_port()
    if any("{port}" in part for part in command):
        command = [part.replace("{port}", str(port)) for part in command]
    else:
        command = [*command, str(port)]
    log = tempfile.TemporaryFile()
    kwargs: dict[str, object] = {"start_new_session": True} if os.name != "nt" else {}
    process = subprocess.Popen(resolve(command), stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                               env=child_env(), **kwargs)  # type: ignore[call-overload]
    try:
        if not wait_for_port(port, process, timeout):
            print(f"FAIL: the server did not start listening on port {port}")
            log.seek(0)
            for line in log.read().decode("utf-8", errors="replace").splitlines()[-10:]:
                print(f"  {line}")
            return None
        print(f"server is up on port {port}")
        return transcript(port)
    finally:
        stop(process)
        log.close()


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main(argv: list[str]) -> int:
    if "--" not in argv or argv.index("--") == 0:
        print("usage: check.py TASK [--expected FILE] [--timeout SECS] [--write] -- COMMAND [ARGS...]")
        return 2
    split = argv.index("--")
    options, command = argv[:split], argv[split + 1:]
    task = options[0].upper() if options[0].lower() == "b" else options[0].zfill(2) if options[0].isdigit() else options[0]
    expected_file = expected_path(task)
    timeout = 120.0
    write = "--write" in options
    if "--expected" in options:
        expected_file = Path(options[options.index("--expected") + 1])
    if "--timeout" in options:
        timeout = float(options[options.index("--timeout") + 1])
    if not command:
        print("FAIL: no command after --")
        return 2
    if not write and not expected_file.exists():
        print(f"FAIL: no expected output found for task {task} ({expected_file})")
        return 2

    print(f"task {task}: {' '.join(command)}")
    if task in TEST_TASKS:
        names = required_tests(expected_file)
        output, code = run_tests(command, timeout)
        if code != 0:
            print(f"FAIL: the test run exited with code {code} (a test failed or did not compile)")
            for line in output.strip().splitlines()[-15:]:
                print(f"  {line}")
            return 1
        actual = check_tests(names, output)
    elif task in API_TASKS:
        result = run_api(command, timeout)
        if result is None:
            return 1
        actual = result
    else:
        try:
            text, _ = run_plain(task, command, timeout)
        except subprocess.TimeoutExpired:
            print(f"FAIL: still running after {timeout:.0f} seconds (waiting for input?)")
            return 1
        if text is None:
            print("FAIL: the output is not UTF-8. Make the program print UTF-8 (see Language notes: the £ sign)")
            return 1
        actual = normalise(text)

    if write:
        expected_file.parent.mkdir(parents=True, exist_ok=True)
        expected_file.write_text("\n".join(actual) + "\n", encoding="utf-8", newline="\n")
        print(f"wrote {expected_file} ({len(actual)} lines)")
        return 0
    expected = normalise(expected_file.read_text(encoding="utf-8"))
    return 0 if compare(expected, actual) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

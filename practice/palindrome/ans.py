import re

# Palindrome Task
potential_palindrome = ["A man, a plan, a canal, Panama!", "Was it a car or a cat I saw?",
                        "No 'x' in Nixon.", "Eva, can I see bees in a cave?!@!!", "Madam, in Eden, I'm Adam!!%%!!!@@",
                        "thing"]


# Remove all non-alphanumeric characters (anything that isn't a letter or number).
def is_palindrome_no_re(input_str: str):
    for char in input_str:
        if char in "?!@%,£$().' ''":
            input_str = input_str.replace(char, '')
    # Convert the string to lowercase to ensure the palindrome check is case-insensitive.
    input_str = input_str.lower()

    # Check if the cleaned string is the same as its reverse using slicing ([::-1]).
    return input_str == input_str[::-1]


def is_palindrome_re(input_str: str):
    pattern = re.compile(r"[^a-zA-Z0-9]") # Potential pre-compile best practice, adds usability, etc.
    cleaned_text = re.sub(pattern, "", input_str).lower()
    return cleaned_text == cleaned_text[::-1]


# Testing area!
for pal_str in potential_palindrome:
    # print(f"{is_palindrome_no_re(pal_str)}")
    print(f"{is_palindrome_re(pal_str)}")

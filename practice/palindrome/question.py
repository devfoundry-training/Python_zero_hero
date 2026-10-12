# ============================================================
# Task: Palindrome Checker
# ============================================================
# Write two functions: one with regex, one without.
# Each should return True if the input is a palindrome,
# ignoring case, spaces, and punctuation.
# ============================================================
potential_palindrome = ["A man, a plan, a canal, Panama!", "Was it a car or a cat I saw?",
                        "No 'x' in Nixon.", "Eva, can I see bees in a cave?!@!!", "Madam, in Eden, I'm Adam!!%%!!!@@",
                        "thing"]

# Solved with and without regex :)
# Remove all non-alphanumeric characters (anything that isn't a letter or number).
# Convert the string to lowercase to ensure the palindrome check is case-insensitive.
# Check if the cleaned string is the same as its reverse using slicing ([::-1]).


# Testing area!
for pal_str in potential_palindrome:
    print(f"{is_palindrome_no_re(pal_str)}")
    print(f"{is_palindrome_re(pal_str)}")

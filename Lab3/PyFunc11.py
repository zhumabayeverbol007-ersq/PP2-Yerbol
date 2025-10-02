def is_palindrome(s):
    s = s.replace(" ", "").lower()
    return s == s[::-1]

test_strings = ["madam", "racecar", "hello"]
for s in test_strings:
    print(f"'{s}' is palindrome: {is_palindrome(s)}")
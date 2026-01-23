def is_palindrome(s):
    s = ''.join(s.lower().split())
    return s == s[::-1]

print(is_palindrome("A man a plan a canal Panama"))  # True
print(is_palindrome("hello"))  # False
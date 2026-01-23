def is_palindrome(s):
    # 清理字符串：转小写、去空格、去标点
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    # 方法1：使用切片比较
    return cleaned == cleaned[::-1]


print(is_palindrome("A man a plan a canal Panama"))      # True
print(is_palindrome("hello"))     # False

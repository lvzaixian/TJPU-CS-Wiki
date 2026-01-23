def compress_string(s):
    if not s:
        return s
    
    compressed = []
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            count += 1
        else:
            compressed.append(s[i-1] + str(count))
            count = 1
    
    compressed.append(s[-1] + str(count))
    result = ''.join(compressed)
    
    return result if len(result) < len(s) else s

# 测试
test_strings = ["aabcccccaaa", "abc", "aaabbc", "a"]
for s in test_strings:
    result = compress_string(s)
    print(f"'{s}' -> '{result}'")
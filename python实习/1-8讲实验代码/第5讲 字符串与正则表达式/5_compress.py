def compress_string(s):
    if not s:
        return s

    compressed = []
    count = 1
    current_char = s[0]

    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            compressed.append(current_char + str(count))
            current_char = s[i]
            count = 1
    # 添加最后一个字符
    compressed.append(current_char + str(count))

    result = ''.join(compressed)
    # 如果压缩后没有变短，返回原字符串
    return result if len(result) < len(s) else s

print(compress_string("aabcccccaaa"))

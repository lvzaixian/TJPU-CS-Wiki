import re


def format_phone_numbers_in_file(input_file, output_file):
    """
    将文件中的电话号码统一格式
    支持格式:
    - 1234567890
    - 123-456-7890
    - 123.456.7890
    - (123)456-7890
    - (123) 456-7890
    统一为: (123) 456-7890
    """

    # 匹配各种电话号码格式的正则表达式
    phone_pattern = r'''
        \(?(\d{3})\)?  # 区号，可能有括号
        [\s\-\.]?      # 可选的分隔符（空格、短横线、点号）
        (\d{3})        # 前三位
        [\s\-\.]?      # 可选的分隔符
        (\d{4})        # 后四位
    '''

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换函数
    def format_phone(match):
        area_code = match.group(1)
        first_three = match.group(2)
        last_four = match.group(3)
        return f"({area_code}) {first_three}-{last_four}"

    # 执行替换
    formatted_content = re.sub(phone_pattern, format_phone, content, flags=re.VERBOSE)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_content)

    print(f"电话号码格式化完成！输出文件: {output_file}")


# 测试文件内容示例
test_content = """
联系人信息：
张三: 1234567890
李四: 123-456-7890
王五: 123.456.7890
赵六: (123)456-7890
钱七: (123) 456-7890
"""

# 创建测试文件
with open('contacts.txt', 'w', encoding='utf-8') as f:
    f.write(test_content)

# 执行替换
format_phone_numbers_in_file('contacts.txt', 'contacts_formatted.txt')

# 查看结果
with open('contacts_formatted.txt', 'r', encoding='utf-8') as f:
    print("格式化结果:")
    print(f.read())


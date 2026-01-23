import re

def format_phone_number(phone):
    """
    将各种格式的电话号码统一为 (XXX) XXX-XXXX 格式
    """
    # 移除非数字字符
    digits = re.sub(r'\D', '', phone)
    
    # 检查是否为10位数字
    if len(digits) != 10:
        raise ValueError("电话号码必须是10位数字")
    
    # 格式化为统一格式
    formatted = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return formatted

# 测试示例
def test_phone_formatting():
    test_numbers = [
        "1234567890",
        "123-456-7890", 
        "123.456.7890",
        "(123)456-7890",
        "(123) 456-7890"
    ]
    
    print("电话号码格式统一测试:")
    for phone in test_numbers:
        try:
            formatted = format_phone_number(phone)
            print(f"原始: {phone:15} -> 统一: {formatted}")
        except ValueError as e:
            print(f"错误: {phone} - {e}")

if __name__ == "__main__":
    test_phone_formatting()
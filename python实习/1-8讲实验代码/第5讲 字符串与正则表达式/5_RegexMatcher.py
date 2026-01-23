import re

class RegexMatcher:
    def __init__(self):
        # 定义所有正则表达式模式
        self.patterns = {
            'positive_integer': r'^[1-9]\d*$',  # 正整数
            'negative_integer': r'^-\d+$',  # 负整数
            'integer': r'^-?\d+$',  # 整数
            'uppercase_letters': r'^[A-Z]+$',  # 大写字母
            'lowercase_letters': r'^[a-z]+$',  # 小写字母
            'letters': r'^[A-Za-z]+$',  # 英文字母
            'alphanumeric': r'^[A-Za-z0-9]+$',  # 字母和数字
            'china_postal_code': r'^[1-9]\d{5}$',  # 中国邮编
            'id_card': r'(^\d{15}$)|(^\d{17}(\d|X|x)$)'  # 身份证
        }

    def match_pattern(self, pattern_name, text):
        """匹配指定模式的文本"""
        if pattern_name not in self.patterns:
            return False, f"未知模式: {pattern_name}"

        pattern = self.patterns[pattern_name]
        is_match = bool(re.match(pattern, text))
        return is_match, f"'{text}' {'符合' if is_match else '不符合'} {pattern_name} 格式"


# 测试函数
def test_regex_patterns():
    """测试所有正则表达式模式"""
    matcher = RegexMatcher()

    # 测试数据
    test_cases = [
        # (模式名称, 测试文本, 期望结果)
        ('positive_integer', '123', True),
        ('positive_integer', '0', False),
        ('positive_integer', '-123', False),
        ('positive_integer', '0123', False),

        ('negative_integer', '-123', True),
        ('negative_integer', '123', False),
        ('negative_integer', '-0', False),

        ('integer', '123', True),
        ('integer', '-123', True),
        ('integer', '0', True),
        ('integer', '12.3', False),

        ('uppercase_letters', 'ABC', True),
        ('uppercase_letters', 'abc', False),
        ('uppercase_letters', 'ABc', False),
        ('uppercase_letters', 'ABC123', False),

        ('lowercase_letters', 'abc', True),
        ('lowercase_letters', 'ABC', False),
        ('lowercase_letters', 'abC', False),

        ('letters', 'Hello', True),
        ('letters', 'HELLO', True),
        ('letters', 'hello', True),
        ('letters', 'Hello123', False),

        ('alphanumeric', 'Hello123', True),
        ('alphanumeric', 'ABC123', True),
        ('alphanumeric', 'abc123', True),
        ('alphanumeric', 'Hello@123', False),

        ('china_postal_code', '100000', True),
        ('china_postal_code', '061001', True),
        ('china_postal_code', '000000', False),
        ('china_postal_code', '12345', False),

        ('id_card', '110101199001011234', True),  # 18位
        ('id_card', '11010119900101123X', True),  # 18位以X结尾
        ('id_card', '110101900101123', True),  # 15位
        ('id_card', '12345678901234567', False),  # 17位
        ('id_card', '1234567890123456789', False)  # 19位
    ]

    print("=" * 60)
    print("正则表达式测试结果")
    print("=" * 60)

    for pattern_name, test_text, expected in test_cases:
        result, message = matcher.match_pattern(pattern_name, test_text)
        status = "✓" if result == expected else "✗"
        print(f"{status} {message}")

    print("=" * 60)


if __name__ == '__main__':
    test_regex_patterns()
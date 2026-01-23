import re

def match_positive_integer(s):
    return bool(re.match(r"^[1-9]\d*$", s))

def match_negative_integer(s):
    return bool(re.match(r"^-\d+$", s))

def match_integer(s):
    return bool(re.match(r"^-?\d+$", s))

def match_uppercase(s):
    return bool(re.match(r"^[A-Z]+$", s))

def match_lowercase(s):
    return bool(re.match(r"^[a-z]+$", s))

def match_letters(s):
    return bool(re.match(r"^[A-Za-z]+$", s))

def match_alphanumeric(s):
    return bool(re.match(r"^[A-Za-z0-9]+$", s))

def match_zipcode(s):
    return bool(re.match(r"^[1-9]\d{5}$", s))

def match_id_card(s):
    return bool(re.match(r"^(\d{15}|\d{17}[\dXx])$", s))

# 测试
print("正整数测试:", match_positive_integer("123"))
print("负整数测试:", match_negative_integer("-456"))
print("身份证测试:", match_id_card("11010119900101123X"))
print("邮政编码测试:", match_zipcode("300384"))
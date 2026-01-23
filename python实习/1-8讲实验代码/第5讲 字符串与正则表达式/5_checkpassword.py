def check_password_strength(password):
    issues = []

    # 检查长度
    if len(password) < 8:
        issues.append("长度不足8位")

    # 检查大写字母
    if not any(c.isupper() for c in password):
        issues.append("缺少大写字母")

    # 检查小写字母
    if not any(c.islower() for c in password):
        issues.append("缺少小写字母")

    # 检查数字
    if not any(c.isdigit() for c in password):
        issues.append("缺少数字")

    # 检查特殊字符
    special_chars = "!@#$%^&*"
    if not any(c in special_chars for c in password):
        issues.append("缺少特殊字符")

    # 确定强度等级
    passed_rules = 5 - len(issues)
    if passed_rules <= 1:
        strength = "弱"
    elif passed_rules <= 3:
        strength = "中"
    else:
        strength = "强"

    return {'strength': strength, 'issues': issues}

password="1234rt*"
print(check_password_strength(password))

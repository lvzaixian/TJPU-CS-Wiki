def check_password_strength(password):
    rules = [
        len(password) >= 8,
        any(c.islower() for c in password) and any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in "!@#$%^&*" for c in password)
    ]
    
    score = sum(rules)
    
    if score == 4:
        return "强"
    elif score >= 2:
        return "中"
    else:
        return "弱"

# 测试
while True:
    pwd = input("输入密码: ")
    if pwd == "quit":
        break
    strength = check_password_strength(pwd)
    print(f"强度: {strength}")
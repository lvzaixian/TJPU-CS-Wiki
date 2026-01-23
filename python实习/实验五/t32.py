import re

def validate_password():
    pattern = r"^[A-Z]{2}[a-z]{2}\d{2}[\$&#\*]{2}$"
    
    while True:
        password = input("请输入密码：")
        if re.match(pattern, password):
            print("密码符合要求！")
            break
        else:
            print("密码格式错误！请确保：前2位大写字母，接着2位小写字母，接着2位数字，最后2位特殊字符($&#*)")

validate_password()
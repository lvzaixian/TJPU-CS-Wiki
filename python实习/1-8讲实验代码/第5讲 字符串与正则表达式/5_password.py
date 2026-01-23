import re
while True:
    pwd=input("please input password:")
    if len(pwd)!=8:
        print("密码长度不符合，请修改！")
        continue
    s_pwd = r"[A-Z]{2}[a-z]{2}[0-9]{2}[$ & * #]{2}"
    pattern= re.compile(s_pwd)
    if pattern.findall(pwd):
        print("密码强度符合要求！")
        break
    else:
        print("密码设定不符合要求，请修改！")
        continue


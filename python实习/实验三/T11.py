# 方法1：使用if-elif-else语句
num = float(input("请输入一个数字："))

if num > 0:
    print("这是一个正数")
elif num < 0:
    print("这是一个负数")
else:
    print("这是零")

# 方法2：使用嵌套的if语句
num = float(input("请输入一个数字："))

if num >= 0:
    if num > 0:
        print("这是一个正数")
    else:
        print("这是零")
else:
    print("这是一个负数")
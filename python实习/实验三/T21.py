n = int(input("请输入一个非负整数："))
if n < 0:
    print("阶乘只能计算非负整数")
else:
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
    print(f"{n}! = {factorial}")
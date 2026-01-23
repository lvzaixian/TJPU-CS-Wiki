# 求指定区间内的阿姆斯特朗数（水仙花数）
start = int(input("请输入区间的起始值："))
end = int(input("请输入区间的结束值："))

print(f"{start}到{end}之间的阿姆斯特朗数（水仙花数）有：")
found = False

for num in range(start, end + 1):
    # 计算数字的位数
    n = len(str(num))
    
    # 计算各位数字的n次方之和
    sum_of_powers = 0
    temp = num
    while temp > 0:
        digit = temp % 10
        sum_of_powers += digit ** n
        temp //= 10
    
    # 判断是否为阿姆斯特朗数
    if sum_of_powers == num:
        print(num, end=" ")
        found = True

if not found:
    print("该区间内没有阿姆斯特朗数（水仙花数）")
else:
    print()  # 换行
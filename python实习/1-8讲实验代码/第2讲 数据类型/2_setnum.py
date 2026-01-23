import random

# 获取用户输入的N值
n = int(input("请输入要生成的随机整数个数N: "))

# 随机生成N个1~1000之间的整数
random_numbers = [random.randint(1, 1000) for _ in range(n)]

print(f"生成的{n}个随机数: {random_numbers}")

# 使用集合去重，然后转换回列表并排序
unique_sorted_numbers = sorted(set(random_numbers))

print(f"去重排序后的学号列表: {unique_sorted_numbers}")
print(f"原始数量: {n}, 去重后数量: {len(unique_sorted_numbers)}")
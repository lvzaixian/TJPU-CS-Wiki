# 输入5个名字
names = input("请输入5个名字（用逗号分隔）: ").split(',')
names = [name.strip() for name in names]

# （1）打印名字列表
print("名字列表:", names)

# （2）输出排序后的列表
sorted_names = sorted(names)
print("排序后:", sorted_names)

# （3）替换名字
print("当前名字:", names)
index = int(input("要替换的名字位置 (1-5): ")) - 1
new_name = input("新名字: ").strip()

names[index] = new_name
print("新列表:", names)
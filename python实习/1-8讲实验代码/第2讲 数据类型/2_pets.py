# 创建5个宠物字典
pet1 = {"type": "狗", "owner": "张三"}
pet2 = {"type": "猫", "owner": "李四"}
pet3 = {"type": "兔子", "owner": "王五"}
pet4 = {"type": "鹦鹉", "owner": "赵六"}
pet5 = {"type": "金鱼", "owner": "钱七"}

# 将字典存储在列表中
pets = [pet1, pet2, pet3, pet4, pet5]

# 遍历列表并打印每个宠物的信息
for i, pet in enumerate(pets, 1):
    print(f"宠物{i}: 类型-{pet['type']}, 主人-{pet['owner']}")
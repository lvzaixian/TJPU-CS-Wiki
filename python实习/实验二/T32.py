# 宠物信息管理程序
def main():
    # 创建5个宠物字典
    pets = [
        {"type": "狗", "owner": "张三"},
        {"type": "猫", "owner": "李四"},
        {"type": "兔子", "owner": "王五"},
        {"type": "鹦鹉", "owner": "赵六"},
        {"type": "金鱼", "owner": "钱七"}
    ]
 
    print("=== 宠物信息列表 ===")
    
    # 遍历并打印每个宠物的信息
    for i, pet in enumerate(pets, 1):
        print(f"{i}. 宠物类型: {pet['type']}, 主人姓名: {pet['owner']}")
    
    # 询问用户是否要添加新宠物
    add_new = input("\n是否要添加新宠物？(y/n): ").lower()
    if add_new == 'y':
        pet_type = input("请输入宠物类型: ")
        owner_name = input("请输入主人姓名: ")
        pets.append({"type": pet_type, "owner": owner_name})
        print("新宠物已添加!")
        
        # 打印更新后的列表
        print("\n=== 更新后的宠物信息列表 ===")
        for i, pet in enumerate(pets, 1):
            print(f"{i}. 宠物类型: {pet['type']}, 主人姓名: {pet['owner']}")

if __name__ == "__main__":
    main()
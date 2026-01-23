# name_management.py
def main():
    print("=== 名字管理程序 ===")
    # 获取5个名字输入
    names_input = input("请输入5个名字，用逗号分隔（例如：Tony, Paul, Nick, Michel, Kevin）: ")
    
    # 处理输入，分割并去除多余空格
    names_list = [name.strip() for name in names_input.split(',')]
    
    # 确保有5个名字，如果不足则补充，如果多余则截取
    if len(names_list) < 5:
        print(f"您只输入了{len(names_list)}个名字，请补充剩余名字。")
        for i in range(len(names_list), 5):
            new_name = input(f"请输入第{i+1}个名字: ")
            names_list.append(new_name.strip())
    elif len(names_list) > 5:
        print(f"您输入了{len(names_list)}个名字，只保留前5个。")
        names_list = names_list[:5]
    
    # (1) 打印原始名字列表
    print("\n(1) 您输入的名字列表:")
    print(names_list)
    
    # (2) 打印排序后的名字列表
    sorted_names = sorted(names_list)
    print("\n(2) 排序后的名字列表:")
    print(sorted_names)
    
    # (3) 替换名字
    print("\n(3) 名字替换")
    print("当前名字列表:")
    for i, name in enumerate(names_list, 1):
        print(f"{i}. {name}")
    
    try:
        index = int(input("\n请输入要替换的名字的编号 (1-5): ")) - 1
        if 0 <= index < 5:
            new_name = input("请输入新名字: ").strip()
            names_list[index] = new_name
            print("\n替换后的新名字列表:")
            print(names_list)
        else:
            print("无效的编号，请输入1-5之间的数字。")
    except ValueError:
        print("输入无效，请输入数字。")

if __name__ == "__main__":
    main()
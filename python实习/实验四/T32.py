def horse_problem():
    """
    百马百担问题求解
    大马驮3担，中马驮2担，2匹小马驮1担
    100匹马驮100担货，求各种马的数量
    """
    solutions = []
    
    # 遍历大马的可能数量
    for big in range(0, 34):  # 大马最多33匹(100/3)
        # 遍历中马的可能数量
        for medium in range(0, 51):  # 中马最多50匹(100/2)
            small = 100 - big - medium  # 小马数量
            
            if small < 0:
                continue
                
            # 检查货物总量
            if big * 3 + medium * 2 + small * 0.5 == 100:
                solutions.append((big, medium, small))
    
    return solutions

# 求解并输出结果
print("=== 百马百担问题解决方案 ===")
solutions = horse_problem()

if solutions:
    print(f"共有 {len(solutions)} 种解决方案:")
    print("大马\t中马\t小马")
    print("-" * 20)
    for big, medium, small in solutions:
        # 验证
        total_horses = big + medium + small
        total_load = big * 3 + medium * 2 + small * 0.5
        print(f"{big}\t{medium}\t{small}")
else:
    print("无解")
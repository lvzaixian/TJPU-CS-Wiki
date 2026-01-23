# 学号去重排序程序
import random

def main():
    print("=== 学号去重排序程序 ===")
    
    try:
        # 获取用户输入的N值
        n = int(input("请输入需要生成的随机整数个数(N): "))
        
        if n <= 0:
            print("请输入一个正整数!")
            return
        
        # 生成N个1~1000之间的随机整数
        random_numbers = [random.randint(1, 1000) for _ in range(n)]
        print(f"\n生成的随机数字: {random_numbers}")
        
        # 去重
        unique_numbers = list(set(random_numbers))
        print(f"去重后的数字: {unique_numbers}")
        
        # 排序
        sorted_numbers = sorted(unique_numbers)
        print(f"排序后的数字: {sorted_numbers}")
        
        # 输出最终结果
        print(f"\n最终筛选出的学号数量: {len(sorted_numbers)}")
        print("按学号从小到大排序的调查顺序:")
        for i, num in enumerate(sorted_numbers, 1):
            print(f"{i}. {num}")
            
    except ValueError:
        print("输入无效，请输入一个整数!")

if __name__ == "__main__":
    main()
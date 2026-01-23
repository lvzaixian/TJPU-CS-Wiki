def is_prime(num):
    """判断一个数是否为素数"""
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    
    # 检查从3到sqrt(num)的奇数
    for i in range(3, int(num**0.5) + 1, 2):
        if num % i == 0:
            return False
    return True

def goldbach_conjecture(n):
    """
    验证哥德巴赫猜想并输出所有素数分解
    
    Args:
        n: 大于2的偶数
    """
    if n <= 2 or n % 2 != 0:
        print("错误：请输入大于2的偶数")
        return
    
    decompositions = []
    
    # 寻找所有素数对
    for p in range(2, n // 2 + 1):
        q = n - p
        if is_prime(p) and is_prime(q):
            decompositions.append((p, q))
    
    # 输出结果
    print(f"=== {n} 的哥德巴赫猜想验证 ===")
    
    if decompositions:
        print(f"{n} 符合哥德巴赫猜想，共有 {len(decompositions)} 种素数分解:")
        for p, q in decompositions:
            print(f"{n} = {p} + {q}")
    else:
        print(f"{n} 不符合哥德巴赫猜想（这种情况不应该出现）")

# 测试代码
def test_goldbach():
    """测试哥德巴赫猜想"""
    test_numbers = [24, 36, 50, 100]
    
    for num in test_numbers:
        goldbach_conjecture(num)
        print()  # 空行分隔

# 运行测试
test_goldbach()

# 也可以让用户输入
try:
    user_input = int(input("请输入一个大于2的偶数: "))
    goldbach_conjecture(user_input)
except ValueError:
    print("输入错误，请输入一个整数")
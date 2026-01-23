def gcd(a, b):
    """计算最大公约数"""
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    """计算最小公倍数"""
    return a * b // gcd(a, b)

# 测试程序
def test_gcd_lcm():
    print("=== 最大公约数和最小公倍数测试 ===")
    
    test_cases = [(12, 18), (15, 25), (7, 13), (48, 36)]
    
    for a, b in test_cases:
        gcd_result = gcd(a, b)
        lcm_result = lcm(a, b)
        print(f"gcd({a}, {b}) = {gcd_result}")
        print(f"lcm({a}, {b}) = {lcm_result}")
        print(f"验证: {a} × {b} = {a * b}, gcd × lcm = {gcd_result * lcm_result}")
        print("-" * 30)

# 运行测试
test_gcd_lcm()
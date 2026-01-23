
def fibonacci_recursive(n):
    """
    递归斐波那契数列
    注意：存在大量重复计算，效率低
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n):
    """
    递推斐波那契数列
    效率高，无重复计算
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


#

# 测试
print("=== 斐波那契数列 ===")
n = 10
print(f"F({n}) = 递归:{fibonacci_recursive(n)}, 递推:{fibonacci_iterative(n)}")

# 性能对比
import time


def benchmark_fibonacci():
    n = 30
    print(f"\n性能对比 (n={n}):")

    # 递推版本
    start = time.time()
    result1 = fibonacci_iterative(n)
    time1 = time.time() - start


    # 朴素递归（n较大时会很慢）
    if n <= 35:
        start = time.time()
        result3 = fibonacci_recursive(n)
        time3 = time.time() - start
    else:
        result3 = "跳过"
        time3 = "太长"

    print(f"递推: {result1}, 时间: {time1:.6f}s")
    print(f"朴素递归: {result3}, 时间: {time3}")


benchmark_fibonacci()
print()



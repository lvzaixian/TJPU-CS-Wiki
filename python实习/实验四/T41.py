import time

def fibonacci_recursive(n):
    """递归方式实现斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

def fibonacci_iterative(n):
    """递推方式实现斐波那契数列"""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    return b

def compare_fibonacci():
    """比较两种实现方式的性能"""
    test_values = [5, 10, 15, 20, 25, 30]
    
    print("=== 斐波那契数列性能对比 ===")
    print("n\t递归时间\t递推时间\t递归结果\t递推结果")
    print("-" * 60)
    
    for n in test_values:
        # 测试递归方式
        start_time = time.time()
        result_recursive = fibonacci_recursive(n)
        time_recursive = time.time() - start_time
        
        # 测试递推方式
        start_time = time.time()
        result_iterative = fibonacci_iterative(n)
        time_iterative = time.time() - start_time
        
        print(f"{n}\t{time_recursive:.6f}s\t{time_iterative:.6f}s\t{result_recursive}\t\t{result_iterative}")

# 运行比较
compare_fibonacci()
def number_statistics(*numbers):
    """
    接收任意数量数字，返回统计信息
    
    Args:
        *numbers: 任意数量的数字参数
        
    Returns:
        dict: 包含数量、求和、均值、最大值、最小值的字典
    """
    if not numbers:
        return {
            'count': 0,
            'sum': 0,
            'mean': 0,
            'max': None,
            'min': None
        }
    
    count = len(numbers)
    total = sum(numbers)
    mean = total / count
    max_val = max(numbers)
    min_val = min(numbers)
    
    return {
        'count': count,
        'sum': total,
        'mean': mean,
        'max': max_val,
        'min': min_val
    }

# 测试代码
result = number_statistics(85, 90, 78, 92, 88)
print("统计结果:")
for key, value in result.items():
    print(f"{key}: {value}")
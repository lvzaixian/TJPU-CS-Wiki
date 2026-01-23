def number_statistics(*numbers):

    # 处理没有参数的情况
    if not numbers:
        return {
            "count": 0,
            "sum": 0,
            "average": 0,
            "max": None,
            "min": None,
            "numbers": ()
        }

    # 计算统计信息
    count = len(numbers)
    total = sum(numbers)
    average = total / count
    maximum = max(numbers)
    minimum = min(numbers)

    return {
        "count": count,
        "sum": total,
        "average": average,
        "max": maximum,
        "min": minimum,
        "numbers": numbers
    }


result = number_statistics(10, 20, 30, 40, 50)
print(f"数字数量: {result['count']}")
print(f"总和: {result['sum']}")
print(f"平均值: {result['average']:.2f}")
print(f"最大值: {result['max']}")
print(f"最小值: {result['min']}")
print(f"数字列表: {result['numbers']}")
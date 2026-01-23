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


def analyze_grades(*scores):
    """分析学生成绩"""
    stats = number_statistics(*scores)

    print("成绩分析报告")
    print("=" * 30)
    print(f"学生人数: {stats['count']}")
    print(f"总分: {stats['sum']}")
    print(f"平均分: {stats['average']:.1f}")
    print(f"最高分: {stats['max']}")
    print(f"最低分: {stats['min']}")



    avg = stats['average']
    if avg >= 90:
      grade = "优秀"
    elif avg >= 80:
      grade = "良好"
    elif avg >= 70:
      grade = "中等"
    elif avg >= 60:
      grade = "及格"
    else:
      grade = "不及格"

    print(f"总体评级: {grade}")
    print("=" * 30)



# 使用示例
print("=== 成绩分析 ===")
analyze_grades(85, 92, 78, 96, 88, 74, 91, 83)

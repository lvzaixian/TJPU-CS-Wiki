def analyze_grades(student_grades):
    """
    对学生成绩进行统计分析并评级
    
    Args:
        student_grades: 学生成绩字典 {姓名: 成绩}
    """
    if not student_grades:
        print("没有学生成绩数据")
        return
    
    grades = list(student_grades.values())
    
    # 统计信息
    count = len(grades)
    total = sum(grades)
    average = total / count
    max_grade = max(grades)
    min_grade = min(grades)
    
    # 评级
    if average >= 90:
        rating = "优秀"
    elif average >= 80:
        rating = "良好"
    elif average >= 70:
        rating = "中等"
    elif average >= 60:
        rating = "及格"
    else:
        rating = "不及格"
    
    # 输出结果
    print("=== 学生成绩分析报告 ===")
    print(f"学生人数: {count}")
    print(f"总分: {total}")
    print(f"平均分: {average:.2f}")
    print(f"最高分: {max_grade}")
    print(f"最低分: {min_grade}")
    print(f"总体评级: {rating}")
    
    print("\n各学生成绩:")
    for name, grade in student_grades.items():
        print(f"  {name}: {grade}分")

# 测试代码
students = {
    "张三": 85,
    "李四": 92,
    "王五": 78,
    "赵六": 88,
    "钱七": 95
}
analyze_grades(students)
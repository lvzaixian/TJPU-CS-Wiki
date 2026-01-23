import csv
def student_analysis():
    students = []

    with open('student.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['语文'] = int(row['语文'])
            row['数学'] = int(row['数学'])
            row['英语'] = int(row['英语'])
            students.append(row)

    print("=== 数据筛选与过滤 ===\n")

    # 1. 筛选总分大于250分的学生
    print("1. 总分大于250分的学生:")
    high_achievers = [
        s for s in students
        if s['语文'] + s['数学'] + s['英语'] > 250
    ]
    print(high_achievers)
    for student in high_achievers:
        total = student['语文'] + student['数学'] + student['英语']
        print(f"{student['姓名']}: {total}分")

    # 2. 筛选数学成绩优秀的学生
    print("\n2. 数学成绩优秀(>=90分)的学生:")
    math_excellent = [s for s in students if s['数学'] >= 90]
    for student in math_excellent:
        print(f"{student['姓名']}: 数学{student['数学']}分")

    # 3. 筛选有科目不及格的学生
    print("\n3. 有科目不及格(<60分)的学生:")
    failing_students = [
        s for s in students
        if s['语文'] < 60 or s['数学'] < 60 or s['英语'] < 60
    ]
    for student in failing_students if failing_students else [{'姓名': '无'}]:
        if student['姓名'] != '无':
            subjects = []
            if student['语文'] < 60: subjects.append(f"语文{student['语文']}分")
            if student['数学'] < 60: subjects.append(f"数学{student['数学']}分")
            if student['英语'] < 60: subjects.append(f"英语{student['英语']}分")
            print(f"{student['姓名']}: {', '.join(subjects)}")
        else:
            print("无不及格学生")

    # 4. 按总分排序
    print("\n4. 按总分排序:")
    sorted_students = sorted(
        students,
        key=lambda s: s['语文'] + s['数学'] + s['英语'],
        reverse=True
    )
    for student in sorted_students:
        total = student['语文'] + student['数学'] + student['英语']
        print(f"{student['姓名']}: {total}分")


# 运行练习2
student_analysis()

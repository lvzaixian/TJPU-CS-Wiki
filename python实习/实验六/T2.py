import pandas as pd
import numpy as np

class StudentDataProcessor:
    """
    学生成绩数据处理类
    """
    
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        print("原始数据:")
        print(self.df)
        print("\n" + "="*50 + "\n")
    
    def filter_by_total_score(self, threshold=250):
        """筛选总分大于指定阈值的学生"""
        result = self.df[self.df['总分'] > threshold]
        print(f"总分大于{threshold}分的学生:")
        print(result)
        return result
    
    def filter_math_excellent(self, score=90):
        """筛选数学成绩优秀的学生"""
        result = self.df[self.df['数学'] >= score]
        print(f"数学成绩优秀(>={score})的学生:")
        print(result)
        return result
    
    def filter_failed_subjects(self, passing_score=60):
        """筛选有科目不及格的学生"""
        subjects = ['语文', '数学', '英语']
        failed_mask = (self.df[subjects] < passing_score).any(axis=1)
        result = self.df[failed_mask]
        print(f"有科目不及格(<{passing_score})的学生:")
        print(result)
        return result
    
    def sort_by_total_score(self, ascending=False):
        """按总分排序"""
        sorted_df = self.df.sort_values('总分', ascending=ascending)
        order = "降序" if not ascending else "升序"
        print(f"按总分{order}排序:")
        print(sorted_df)
        return sorted_df

def create_sample_data():
    """创建示例CSV文件"""
    data = {
        '学号': [1001, 1002, 1003, 1004, 1005],
        '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
        '语文': [85, 92, 78, 65, 58],
        '数学': [92, 88, 95, 59, 76],
        '英语': [88, 85, 82, 72, 61],
        '总分': [265, 265, 255, 196, 195]
    }
    
    df = pd.DataFrame(data)
    df.to_csv('students.csv', index=False, encoding='utf-8-sig')
    print("示例数据文件已创建: students.csv")

def main():
    # 创建示例数据
    create_sample_data()
    
    # 处理数据
    processor = StudentDataProcessor('students.csv')
    
    # 执行各种筛选和排序
    processor.filter_by_total_score(250)
    print("\n" + "-"*30 + "\n")
    
    processor.filter_math_excellent(90)
    print("\n" + "-"*30 + "\n")
    
    processor.filter_failed_subjects(60)
    print("\n" + "-"*30 + "\n")
    
    processor.sort_by_total_score(ascending=False)

if __name__ == "__main__":
    main()
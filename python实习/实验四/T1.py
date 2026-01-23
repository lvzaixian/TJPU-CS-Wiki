def process_data(data_list):
    """使用Pythonic方式处理数据列表"""
    return [x * 2 if x % 2 == 0 else x * 3 for x in data_list]

# 测试代码
data = [1, 2, 3, 4, 5, 6]
output = process_data(data)
print(f"原始数据: {data}")
print(f"处理结果: {output}")
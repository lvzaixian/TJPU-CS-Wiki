import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 设置非交互式后端
import matplotlib.pyplot as plt


# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建销售数据
np.random.seed(42)
sales_data = {
    '日期': pd.date_range('2024-01-01', periods=100, freq='D'),
    '产品': np.random.choice(['A', 'B', 'C', 'D'], 100),
    '销售额': np.random.randint(100, 5000, 100),
    '数量': np.random.randint(1, 20, 100),
    '地区': np.random.choice(['北京', '上海', '广州', '深圳'], 100)
}

sales_df = pd.DataFrame(sales_data)
print(sales_df)

# 1. 筛选出销售额大于2000的记录
high_sales = sales_df[sales_df['销售额'] > 2000]
print("销售额大于2000的记录:")
print(high_sales)
print(f"共{len(high_sales)}条记录\n")

# 2. 计算每个产品的总销售额和平均销售额
product_sales = sales_df.groupby('产品')['销售额'].agg(['sum', 'mean']).round(2)
product_sales.columns = ['总销售额', '平均销售额']
print("各产品销售统计:")
print(product_sales)
print()

# 3. 找出每个地区销售额最高的产品
region_top = sales_df.loc[sales_df.groupby('地区')['销售额'].idxmax()]
print("每个地区销售额最高的产品:")
print(region_top[['地区', '产品', '销售额']])
print()

# 4. 计算每周的销售总额
weekly_sales = sales_df.groupby(pd.Grouper(key='日期', freq='W'))['销售额'].sum()
print("每周销售总额:")
print(weekly_sales)
print()

# 数据可视化
plt.figure(figsize=(15, 10))

# 1. 各产品销售额的柱状图
plt.subplot(2, 2, 1)
product_total = sales_df.groupby('产品')['销售额'].sum()
plt.bar(product_total.index, product_total.values)
plt.title('各产品总销售额')
plt.xlabel('产品')
plt.ylabel('销售额')

# 2. 销售额随时间变化的折线图
plt.subplot(2, 2, 2)
daily_sales = sales_df.groupby('日期')['销售额'].sum()
plt.plot(daily_sales.index, daily_sales.values)
plt.title('销售额时间趋势')
plt.xlabel('日期')
plt.ylabel('销售额')
plt.xticks(rotation=45)

# 3. 各地区销售额占比的饼图
plt.subplot(2, 2, 3)
region_sales = sales_df.groupby('地区')['销售额'].sum()
plt.pie(region_sales.values, labels=region_sales.index, autopct='%1.1f%%')
plt.title('各地区销售额占比')

# 4. 销售额与数量的散点图
plt.subplot(2, 2, 4)
plt.scatter(sales_df['数量'], sales_df['销售额'])
plt.title('销售额与数量关系')
plt.xlabel('数量')
plt.ylabel('销售额')

plt.tight_layout()
plt.savefig('sales_analysis.png')  # 保存图片而不是显示
print("图表已保存为 sales_analysis.png")
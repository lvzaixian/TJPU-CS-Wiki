import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================= 1. 基础设置 =================

# 设置绘图风格 (ggplot 风格，简洁美观)
plt.style.use('ggplot') 

# 解决中文显示和负号问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置 Pandas 控制台打印格式 (让输出对齐，看起来舒服)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', 180)
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:.2f}'.format # 小数保留2位

# ================= 2. 数据生成 =================
np.random.seed(42)
sales_data = {
    '日期': pd.date_range('2024-01-01', periods=100, freq='D'),
    '产品': np.random.choice(['A', 'B', 'C', 'D'], 100),
    '销售额': np.random.randint(100, 5000, 100),
    '数量': np.random.randint(1, 20, 100),
    '地区': np.random.choice(['北京', '上海', '广州', '深圳'], 100)
}
sales_df = pd.DataFrame(sales_data)

# ================= 3. 数据处理与输出 =================

# --- 要求1：筛选出销售额大于2000的记录 (导出为Excel) ---
high_sales = sales_df[sales_df['销售额'] > 2000]
# index=False 表示不把左边那列序号存进去，表格更干净
high_sales.to_excel('销售额大于2000的记录.xlsx', index=False)
print(f">>> 已将 {len(high_sales)} 条高销售额记录导出为 Excel 文件。")

# --- 要求2：计算每个产品的总销售额和平均销售额 ---
print("\n>>> 各产品销售统计:")
product_stats = sales_df.groupby('产品')['销售额'].agg(['sum', 'mean'])
print(product_stats)

# --- 要求3：找出每个地区销售额最高的产品 ---
print("\n>>> 各地区销售额最高的产品:")
region_group = sales_df.groupby(['地区', '产品'])['销售额'].sum().reset_index()
best_products = region_group.sort_values('销售额', ascending=False).drop_duplicates(['地区'])
print(best_products.sort_values('地区'))

# --- 要求4：计算每周的销售总额 ---
print("\n>>> 每周销售总额 (前5周示例):")
df_temp = sales_df.set_index('日期')
weekly_sales = df_temp.resample('W')['销售额'].sum()
print(weekly_sales.head())

# ================= 4. 绘图与保存 (美化版) =================

# 定义一套清新的配色方案
colors = ['#5DADE2', '#AF7AC5', '#48C9B0', '#F4D03F', '#EB984E']

# 图1：各产品销售额柱状图
plt.figure(figsize=(10, 6))
ax1 = product_stats['sum'].plot(kind='bar', color=colors[:4], width=0.6, edgecolor='white')
plt.title('各产品销售额统计', fontsize=14)
plt.ylabel('总销售额', fontsize=12)
plt.xlabel('产品型号', fontsize=12)
plt.xticks(rotation=0)
# 柱子上标数值
for p in ax1.patches:
    ax1.annotate(str(int(p.get_height())), (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha='center', va='bottom', xytext=(0, 5), textcoords='offset points')
plt.tight_layout()
plt.savefig('1_产品销售额_美化版.png', dpi=300)
plt.close()

# 图2：销售额随时间变化折线图
plt.figure(figsize=(12, 6))
daily_sales = sales_df.groupby('日期')['销售额'].sum()
plt.plot(daily_sales.index, daily_sales.values, color='#E74C3C', linewidth=2, marker='o', markersize=4)
plt.title('2024年销售额趋势', fontsize=14)
plt.xlabel('日期')
plt.ylabel('日销售额')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('2_时间趋势_美化版.png', dpi=300)
plt.close()

# 图3：各地区占比饼图
plt.figure(figsize=(8, 8))
region_sales = sales_df.groupby('地区')['销售额'].sum()
explode = [0.03] * len(region_sales) # 让饼图裂开一点点缝隙
plt.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%', 
        startangle=140, colors=colors, explode=explode, textprops={'fontsize': 12})
plt.title('各地区销售额占比', fontsize=14)
plt.tight_layout()
plt.savefig('3_地区占比_美化版.png', dpi=300)
plt.close()

# 图4：销售额与数量散点图
plt.figure(figsize=(10, 6))
plt.scatter(sales_df['数量'], sales_df['销售额'], color='#8E44AD', alpha=0.6, s=60, edgecolors='white')
plt.title('销售额 vs 销售数量', fontsize=14)
plt.xlabel('数量', fontsize=12)
plt.ylabel('销售额', fontsize=12)
plt.tight_layout()
plt.savefig('4_散点分析_美化版.png', dpi=300)
plt.close()

print("\n>>> 所有图表绘制完成，已保存至文件夹。")
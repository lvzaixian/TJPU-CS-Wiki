# 商品价格
prices = [568, 239, 368, 425, 121, 219, 834, 1263, 26]

# 输入价格区间
min_price = int(input("最低价: "))
max_price = int(input("最高价: "))

# 筛选和排序
filtered = sorted([p for p in prices if min_price <= p <= max_price])

# 输出结果
print("筛选结果:", filtered)
print("平均价格:", sum(filtered) / len(filtered) if filtered else 0)
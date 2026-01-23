# price_filter.py
def main():
    print("=== 商品价格筛选程序 ===")
    prices = [568, 239, 368, 425, 121, 219, 834, 1263, 26]
    print("所有商品价格:", prices)
    
    try:
        # 获取价格区间输入
        min_price = float(input("\n请输入最低价格: "))
        max_price = float(input("请输入最高价格: "))
        
        if min_price > max_price:
            print("最低价格不能高于最高价格，已自动交换数值。")
            min_price, max_price = max_price, min_price
        
        # 筛选价格区间内的商品
        filtered_prices = [price for price in prices if min_price <= price <= max_price]
        
        if not filtered_prices:
            print("在该价格区间内没有商品。")
            return
        
        # 排序
        sorted_prices = sorted(filtered_prices)
        print(f"\n在区间 [{min_price}, {max_price}] 内的商品价格 (从小到大排序):")
        print(sorted_prices)
        
        # 计算平均价格
        average_price = sum(sorted_prices) / len(sorted_prices)
        print(f"该区间商品的平均价格为: {average_price:.2f}")
        
    except ValueError:
        print("输入无效，请输入数字。")

if __name__ == "__main__":
    main()
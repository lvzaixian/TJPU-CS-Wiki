# -*- coding: UTF-8 -*-
# 温度转换实验程序

def celsius_to_fahrenheit(c_temp):
    """把摄氏度转换成华氏度"""
    f_temp = c_temp * 1.8 + 32
    return f_temp

def fahrenheit_to_celsius(f_temp):
    """把华氏度转换成摄氏度"""
    c_temp = (f_temp - 32) / 1.8
    return c_temp

def single_conversion(mode):
    """处理单项温度转换"""
    try:
        if mode == 1:  # 摄氏度转华氏度
            input_temp = float(input("请输入摄氏度温度: "))
            result_temp = celsius_to_fahrenheit(input_temp)
            print(f"{input_temp:.2f}°C = {result_temp:.2f}°F")
        else:  # 华氏度转摄氏度
            input_temp = float(input("请输入华氏度温度: "))
            result_temp = fahrenheit_to_celsius(input_temp)
            print(f"{input_temp:.2f}°F = {result_temp:.2f}°C")
    except ValueError:
        print("输入的不是有效数字，请重新输入")

def dual_conversion():
    """处理双向温度转换"""
    temp_input = input("请输入温度值(例如: 25C 或 77F): ").strip()
    
    if not temp_input:
        print("输入不能为空")
        return
        
    unit = temp_input[-1].upper()
    
    try:
        temp_value = float(temp_input[:-1])
    except ValueError:
        print("温度数值部分无效")
        return
    
    if unit == 'C':
        result = celsius_to_fahrenheit(temp_value)
        print(f"{temp_value:.2f}°C = {result:.2f}°F")
    elif unit == 'F':
        result = fahrenheit_to_celsius(temp_value)
        print(f"{temp_value:.2f}°F = {result:.2f}°C")
    else:
        print("请使用C或F表示温度单位")

def main():
    """程序主函数"""
    print("=" * 40)
    print("         Temperature Converter")
    print("=" * 40)
    
    while True:
        print("\n选择转换模式:")
        print("1. 摄氏度转华氏度")
        print("2. 华氏度转摄氏度")
        print("3. 双向转换(自动识别)")
        print("4. 退出程序")
        
        choice = input("请输入选项(1-4): ").strip()
        
        if choice == '1':
            single_conversion(1)
        elif choice == '2':
            single_conversion(2)
        elif choice == '3':
            dual_conversion()
        elif choice == '4':
            print("感谢使用温度转换程序!")
            break
        else:
            print("无效选项，请重新选择")

# 启动程序
if __name__ == "__main__":
    main()
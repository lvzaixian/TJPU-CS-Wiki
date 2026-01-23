def gcd(x, y):
   """两个数的最大公约数"""
   # 获取最小值
   smaller = (y+1 if x>y else x+1)
   for i in range(1,smaller):
       if((x % i == 0) and (y % i == 0)):
           gcd = i
   return gcd
# 定义函数
def lcm(x, y):
   """两个数的最小公倍数"""
   greater = (x if x>y else y)
   while(True):
       if((greater % x == 0) and (greater % y == 0)):
           lcm = greater
           break
       greater += 1
   return lcm



# 获取用户输入
num1 = int(input("输入第一个数字: "))
num2 = int(input("输入第二个数字: "))
print( num1,"和", num2,"的最小公倍数为", lcm(num1, num2))
print( num1,"和", num2,"的最大公约数为",gcd(num1, num2))

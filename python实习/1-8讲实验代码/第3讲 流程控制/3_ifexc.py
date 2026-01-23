
num = float(input("输入一个数字: "))
if num < 0:
   print("负数")
elif num == 0:
   print("零")
else:
   print("正数")


num = float(input("输入一个数字: "))
if num <= 0:
   if num == 0:
       print("零")
   else:
       print("负数")
else:
   print("正数")


#  Python判断奇数偶数
# 如果是偶数，除以2后余数为0
# 如果是余数，除以2后余数为1
num = int(input("输入一个数字: "))
if (num % 2) != 0:
   print("{0} 是奇数".format(num))
else:
   print("{0} 是偶数".format(num))


#用if语句判断用户输入的年份是否为闰年。
year = int(input("输入一个年份: "))
if (year % 4) == 0:
   if (year % 100) == 0:
       if (year % 400) == 0:
           print("{0} 是闰年".format(year))   # 整百年能被400整除的是闰年
       else:
           print("{0} 不是闰年".format(year))
   else:
       print("{0} 是闰年".format(year))       # 非整百年能被4整除的为闰年
else:
    print("{0} 不是闰年".format(year))



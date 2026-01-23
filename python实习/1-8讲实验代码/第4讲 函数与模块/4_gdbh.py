import math

def gdbh(num):
    flag=0
    if num%2==0 and num>2:
        for j in range(2, num//2+1):
              b11=is_primer(j)
              b12=is_primer(num-j)
              if b11==1 and b12==1:
                    print("{0}={1}+{2}".format(num,j,num-j))
                    flag=1
                    break
    return flag

def is_primer(num):
     flag=1
     if num==1 or num==2:
           flag=1
     else:
           end=int(math.sqrt(num))
           for j in range(2,end):
                if num %j==0:
                     flag=0
     return flag


x=int(input("请输入一个大于2的偶数:"))
while x<2 or x%2==1:
    x= int(input("请输入一个大于2的偶数:"))

if gdbh(x)==1:
    print("{0}能写成两个素数的和，符合哥德巴赫猜想". format(x))
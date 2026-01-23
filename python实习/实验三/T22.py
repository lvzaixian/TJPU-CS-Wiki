print("10以内的素数有：")
for num in range(2, 11):  # 从2开始到10
    is_prime = True
    for i in range(2, num):
        if num % i == 0:
            is_prime = False
            break
    if is_prime:
        print(num, end=" ")
print()  # 换行
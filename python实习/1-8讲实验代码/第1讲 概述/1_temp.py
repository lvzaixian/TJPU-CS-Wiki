
def c2f(cel):
    fah = cel * 1.8 + 32
    return fah


def f2c(fah):
    cel = (fah - 32) / 1.8
    return cel


print('32摄氏度 = %.2f华氏度' % c2f(32))
print('99华氏度 = %.2f摄氏度' % f2c(99))

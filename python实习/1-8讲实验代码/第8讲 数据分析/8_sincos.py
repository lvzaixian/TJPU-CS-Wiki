import matplotlib
matplotlib.use('TkAgg')
import pylab as plt
import numpy as np

x = np.linspace(0, 10, 1000)  # 设置自变量格式
y = np.sin(x) + 1             # 设置因变量y
z = np.cos(x**2) + 1          # 设置因变量z

plt.figure(figsize=(8, 4))    # 设置图像大小
plt.plot(x, y, label="sinx+1", color='red', linewidth=2)  # 作图（x,y），设置标签格式
plt.plot(x, z, label="cosx^2+1")  # 作图（x，z）
plt.xlabel('Time(s)')  # 设置x轴名称
plt.ylabel('Volt')  # 设置y轴名称
plt.title('A simple Example')  # 设置表格标题
plt.ylim(0, 2.2)  # 显示的y轴范围
plt.legend() # 显示图例
plt.show()  # 显示作图结果

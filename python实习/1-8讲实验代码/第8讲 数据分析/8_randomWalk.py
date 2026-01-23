import random
import matplotlib
matplotlib.use('TkAgg')
import pylab as plt


position = 0
walk = [position]
steps = 1000
for i in range(steps):
    step = 1 if random.randint(0, 1) else -1
    position += step
    walk.append(position)

plt.figure(figsize=(8, 4))  # 设置图像大小
plt.plot(walk, color='red', linewidth=1)  # 作图（x,y），设置标签格式
plt.xlabel('Steps')  # 设置x轴名称
plt.ylabel('Value')  # 设置y轴名称
plt.title('A Simple Random Walk')  # 设置表格标题
plt.show()  # 显示作图结果


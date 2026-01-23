import numpy as np
import os, re
import matplotlib.pyplot as plt # 用于绘图
from PIL import Image

# --- 请确保这里的路径是你电脑上图片所在的真实路径 ---
path = './images/'  # 假设图片在当前目录下的images文件夹
# ------------------------------------------------

def getImgNames(path):
    filenames = os.listdir(path)
    imgNames = []
    for i in filenames:
        if re.findall(r'^\d_\d+\.jpg$', i) != []:
            imgNames.append(i)
    return imgNames

imgNames = getImgNames(path)
print(f"步骤1结果：共读取到 {len(imgNames)} 张图片")

# 读取第一张图做演示
img = Image.open(os.path.join(path, imgNames[0]))
M, N = img.size
# 切割
roi = img.crop((M//2-50, N//2-50, M//2+50, N//2+50))

# 绘图展示
plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title("Original Image (With Background)")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(roi)
plt.title("ROI Crop (Water Only)")
plt.axis('off')

plt.show()
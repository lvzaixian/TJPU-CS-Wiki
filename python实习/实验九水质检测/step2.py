import numpy as np
import os, re
from PIL import Image

# ---------------- 配置路径 ----------------
path = './images/'  
# ----------------------------------------

def getImgNames(path):
    filenames = os.listdir(path)
    imgNames = []
    for i in filenames:
        if re.findall(r'^\d_\d+\.jpg$', i) != []:
            imgNames.append(i)
    return imgNames

# 定义三阶矩函数
def Skewness(data=None):
    x = np.mean((data-data.mean())**3)
    return np.sign(x)*abs(x)**(1/3)

imgNames = getImgNames(path)
n = len(imgNames)
print(f"正在处理 {n} 张图片，请稍候...")

data = np.zeros([n, 9])
labels = np.zeros([n])

for i in range(n):
    img = Image.open(os.path.join(path, imgNames[i]))
    M,N = img.size
    img = img.crop((M//2-50,N//2-50,M//2+50,N//2+50))
    r,g,b = img.split()
    rd = np.asarray(r)/255
    gd = np.asarray(g)/255
    bd = np.asarray(b)/255

    # R通道
    data[i,0] = rd.mean()
    data[i,3] = rd.std()
    data[i,6] = Skewness(rd)
    # G通道
    data[i,1] = gd.mean()
    data[i,4] = gd.std()
    data[i,7] = Skewness(gd)
    # B通道
    data[i,2] = bd.mean()
    data[i,5] = bd.std()
    data[i,8] = Skewness(bd)
    
    labels[i] = int(imgNames[i].split('_')[0])

print("-" * 40)
print("【步骤2 运行结果】")
print(f"成功提取图片数量: {n}")
print(f"特征矩阵 data 维度: {data.shape}")
print(f"标签向量 labels 维度: {labels.shape}")
print("-" * 40)
print("样例数据 (第一张图的9个特征值):")
print(np.round(data[0], 4))
print("-" * 40)
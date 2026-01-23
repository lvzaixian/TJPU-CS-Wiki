import numpy as np
import os, re
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# ---------------- 配置路径 ----------------
path = './images/'  
# ----------------------------------------

# --- (复现步骤1和2：数据准备) ---
def getImgNames(path):
    filenames = os.listdir(path)
    imgNames = []
    for i in filenames:
        if re.findall(r'^\d_\d+\.jpg$', i) != []:
            imgNames.append(i)
    return imgNames

def Skewness(data=None):
    x = np.mean((data-data.mean())**3)
    return np.sign(x)*abs(x)**(1/3)

imgNames = getImgNames(path)
n = len(imgNames)
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
    data[i,0] = rd.mean(); data[i,1] = gd.mean(); data[i,2] = bd.mean()
    data[i,3] = rd.std();  data[i,4] = gd.std();  data[i,5] = bd.std()
    data[i,6] = Skewness(rd); data[i,7] = Skewness(gd); data[i,8] = Skewness(bd)
    labels[i] = int(imgNames[i].split('_')[0])

# --- (本步骤核心：步骤3 模型构建) ---
print("-" * 40)
print("正在进行数据切分与模型训练...")

# 1. 数据拆分
# random_state=12 确保和你实验指导书结果一致
data_tr, data_te, label_tr, label_te = train_test_split(data, labels, test_size=0.2, random_state=12)

# 2. 模型训练
# random_state=5 确保决策树生成结果一致
dt_classifier = DecisionTreeClassifier(random_state=5).fit(data_tr, label_tr)

print("-" * 40)
print("【步骤3 运行结果】")
print(f"原始样本总数: {len(labels)}")
print(f"训练集样本数 (Training Set): {len(label_tr)}  (约80%)")
print(f"测试集样本数 (Test Set):     {len(label_te)}   (约20%)")
print(f"模型对象: {dt_classifier}")
print("模型构建完成，已准备好进行预测。")
print("-" * 40)
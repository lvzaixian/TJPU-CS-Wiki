import numpy as np
import os, re
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

# ---------------- 配置路径 ----------------
path = './images/'  
# ----------------------------------------

# --- (复现前三步) ---
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
    rd = np.asarray(r)/255; gd = np.asarray(g)/255; bd = np.asarray(b)/255
    data[i,0] = rd.mean(); data[i,1] = gd.mean(); data[i,2] = bd.mean()
    data[i,3] = rd.std();  data[i,4] = gd.std();  data[i,5] = bd.std()
    data[i,6] = Skewness(rd); data[i,7] = Skewness(gd); data[i,8] = Skewness(bd)
    labels[i] = int(imgNames[i].split('_')[0])

data_tr, data_te, label_tr, label_te = train_test_split(data, labels, test_size=0.2, random_state=12)
dt_classifier = DecisionTreeClassifier(random_state=5).fit(data_tr, label_tr)

# --- (本步骤核心：步骤4 模型评价) ---
print("-" * 40)
print("正在进行模型评价...")

# 预测
pre_te = dt_classifier.predict(data_te)

# 混淆矩阵
cm_te = confusion_matrix(label_te, pre_te)

# 准确率
acc = accuracy_score(label_te, pre_te)

print("-" * 40)
print("【步骤4 运行结果】")
print("1. 混淆矩阵 (Confusion Matrix):")
print(cm_te)
print("\n2. 模型准确率 (Accuracy):")
print(acc)
print("-" * 40)
if acc == 1.0:
    print("结果分析: 完美！所有测试样本均被正确分类。")
else:
    print(f"结果分析: 还可以，准确率为 {acc*100}%")
print("-" * 40)
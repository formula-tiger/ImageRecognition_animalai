from PIL import Image # OpenCVより単純な画像処理にむく
import os, glob
import numpy as np
from sklearn import cross_validation

classes = ["monkey", "boar", "crow"]
num_classes = len(classes)
image_size = 50

# 画像の読み込み

x = []
Y = []
for index, classlabel in enumerate(classes):
    photos_dir = "./" + classlabel
    files = glob.glob.(photos_dir + "/*.jpg")
    for i, file in enumerate(files):
        if i >= 200: break
        # 最小の数に揃えている
        image = Image.open(file)
        image = image.convert("RGB")
        image = image.resize(image_size, image_size) # 縦横一緒なので
        data = np.asarray(image)
        X.append(data)
        Y.append(index)

X = np.array(X)
Y = np.array(Y)


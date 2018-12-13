from PIL import Image # OpenCVより単純な画像処理にむく
import os, glob
import numpy as np
from sklearn import model_selection

classes = ["monkey", "boar", "crow"]
num_classes = len(classes)
image_size = 50

# 画像の読み込み

X = []
Y = []
for index, classlabel in enumerate(classes):
    photos_dir = "./" + classlabel
    files = glob.glob(photos_dir + "/*.jpg")
    for i, file in enumerate(files):
        if i >= 200: break
        # 最小の数に揃えている
        image = Image.open(file)
        image = image.convert("RGB")
        image = image.resize((image_size, image_size))
        # リサイズ後のサイズを(width, height), 縦横一緒なので image_sizeが二つある
        data = np.asarray(image)
        X.append(data)
        Y.append(index)

X = np.array(X)
Y = np.array(Y)

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y)
xy = (X_train, X_test, y_train, y_test)
np.save("./animal.npy", xy)
"""
np.save と np.load でファイルにndarrayを出力したり、ファイルから入力したりできる。
フォーマットはバイナリで、拡張子には.npyを使う
4つの変数を一つのファイルに保存
第一引数にファイル名、第二引数に保存したいオブジェクトを指定, パラメータ、重みも保存
"""
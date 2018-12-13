from PIL import Image # OpenCVより単純な画像処理にむく
import os, glob
import numpy as np
from sklearn import model_selection

classes = ["monkey", "boar", "crow"]
num_classes = len(classes)
image_size = 50
num_testdata = 50

# 画像の読み込み
X_train = []
y_train = []
X_test = []
y_test = []

"""
学習データには X 、クラスラベルに y という変数名がよく使われています。
X が大文字なのは、この値が多次元の値だからです
（数学では行列を大文字で表記することが多い）。
"""

for index, classlabel in enumerate(classes):
    photos_dir = "./" + classlabel
    files = glob.glob(photos_dir + "/*.jpg")
    for i, file in enumerate(files):
        if i >= 122: break  # 最小の数に揃えている
        image = Image.open(file)  # 画像の読み込み（この時点では参照されているだけで、必要になってからデータを読み込む）
        image = image.convert("RGB")
        image = image.resize((image_size, image_size))  # リサイズ後のサイズを(width, height), 縦横一緒なので image_sizeが二つある
        data = np.asarray(image)

        if i < num_testdata:
            X_test.append(data)
            y_test.append(index)
        else:
            for angle in range(-20,20,5):
                # 回転
                img_r = image.rotate(angle)
                data = np.asarray(img_r)
                X_train.append(data)
                y_train.append(index)

                # 反転
                img_trans = img_r.transpose(Image.FLIP_LEFT_RIGHT)  # Image.transpose(method) = 反転
                data = np.asarray(img_trans)
                X_train.append(data)
                y_train.append(index)

# X = np.array(X)
# Y = np.array(Y)
X_train = np.array(X_train)
X_test = np.array(X_test)
y_train = np.array(y_train)
y_test_teste= np.array(y_test)

# X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y)  # train_test_split関数の第1引数に入力データ、第2引数に正解ラベルの配列　シャッフルして分割
xy = (X_train, X_test, y_train, y_test)
np.save("./animal_aug.npy", xy)

"""
np.save と np.load でファイルにndarrayを出力したり、ファイルから入力したりできる。
フォーマットはバイナリで、拡張子には.npyを使う
4つの変数を一つのファイルに保存
第一引数にファイル名、第二引数に保存したいオブジェクトを指定, パラメータ、重みも保存
"""
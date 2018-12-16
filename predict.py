from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
import keras, sys
import numpy as np
from PIL import Image


classes = ["monkey","boar","crow"]
num_classes = len(classes)
image_size = 50


def build_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same', input_shape=(50, 50, 3)))
    # Conv2Dの引数は arg1 が入力テンソル で32"はフィルタ(カーネル)の数を表し、出力の次元である。"(3, 3)" はフィルタ(カーネル)のサイズを表す。
    # input_shape には行列の個数を取り除いた数値を格納, padding とは　入力の特徴マップの周辺をある数値で埋める
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())  # データを一列に並べる 入力を平滑化
    model.add(Dense(512))  # # 通常の全結合NNレイヤー 引数はunit数
    model.add(Activation('relu'))
    model.add(Dropout(0.5))  # 半分捨てる
    model.add(Dense(3))  # 判別したい画像の種類の数
    model.add(Activation('softmax'))

    opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)  # RMSporpは勾配降下法の最適化アルゴリズムの1つ, decayは学習率を1回ごとに下げる比率


    model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])


    # モデルのロード
    model = load_model('./animal_cnn_aug.h5')  # load.modelはkerasのメソッド


    return model

def main():
    image = Image.open(sys.argv[1])
    # python predict.py filename arg0 は 実行ファイル名　arg1は 開くファイルの名前
    image = image.convert('RGB')
    image = image.resize((image_size, image_size))
    data = np.asarray(image)
    X = []
    X.append(data)
    X = np.array(X)
    model = build_model()
    result = model.predict([X])[0]
    predicted = result.argmax()  # 一番、あたいの大きい配列のindexを返す
    percentage = int(result[predicted] * 100)
    print("{0}({1} %)".format(classes[predicted], percentage))


if __name__ == "__main__":
    main()

"""
CNN、ニューラルネット、 TensorFlowに関しては以下のURLがわかりやすい
https://deepinsider.jp/tutor/introtensorflow/whatiscnn
https://deepage.net/deep_learning/2016/11/07/convolutional_neural_network.html
"""

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
import keras
import numpy as np

classes = ["monkey","boar","crow"]
num_classes = len(classes)
image_size = 50


# メインnの関数を定義
def main():
    X_train, X_test, y_train, y_test = np.load("./animal.npy")
    # 正規化をする 0- 256の値のnumpyアレーを最大値で割理、 0-1に収束
    X_train = X_train.astype("float") / 256
    X_test = X_test.astype("float") / 256
    y_train = np_utils.to_categorical(y_train, num_classes)
    # one-hot-vectorに変換　=> [0, 1, 2] を [1, 0, 0], [0, 1, 0], [0, 0, 1]に
    y_test = np_utils.to_categorical(y_test, num_classes)

    model = model_train(X_train, y_train)   # モデルの学習
    model_eval(model, X_test, y_test)       # モデルの評価

def model_train(X, y):
    # モデルの定義
    model = Sequential()
    model.add(Conv2D(32,(3,3), padding='same',input_shape= X.shape[1:]))
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

    model.add(Flatten())     # データを一列に並べる 入力を平滑化
    model.add(Dense(512))    # # 通常の全結合NNレイヤー 引数はunit数
    model.add(Activation('relu'))
    model.add(Dropout(0.5))  # 半分捨てる
    model.add(Dense(3))      # 判別したい画像の種類の数
    model.add(Activation('softmax'))


    # ここから最適化
    opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)  # RMSporpは勾配降下法の最適化アルゴリズムの1つ, decayは学習率を1回ごとに下げる比率

    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])
    """
    loss=損失関数 metrics = 評価の指標 
    accurecy = どれくらい正答したか
    categorical_crossentropy = 多クラスの 交差エントロピーをtrainingでの損失関数として使う
    metrics = モデルの性能を測るために使われる「評価関数」
    """

    model.fit(X, y, batch_size=32, epochs=50)


    """
    batch_size=32 = 1回のトレーニング(エポックと言う)に使うデータの数(32画像)
    nb_epochs=100 = そのトレーニングを何セットするのか (マシンが遅い場合、低めに設定)
    It gets to 75% validation accuracy in 25 epochs, and 79% after 50 epochs.
    """

    model.save('./animal_cnn.h5')  # モデルを指定のディレクトリに保存
    return model


def model_eval(model, X, y):
    scores = model.evaluate(X, y, verbose=1)
    print('Test Loss:', scores[0])
    print('Test Accuracy:', scores[1])



"""
verbose: 0とすると標準出力にログを出力しない．1の場合はログをプログレスバーで標準出力
evaluate関数 バッチごとに、ある入力データにおける損失値を計算 引数：x: 入力データ，Numpy 配列/Numpy 配列リスト y: ラベル，Numpy 配列
    戻り値：スカラーのリスト（モデルが他の評価関数(Accurecyなど)を計算している場合）

"""

if __name__ == "__main__":
    main()


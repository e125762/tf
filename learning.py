import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation, RepeatVector
from keras.layers import LSTM
from keras.layers.wrappers import TimeDistributed
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle


#パディング
def padding(chars, maxlen):
  return chars + ' ' * (maxlen - len(chars))

text = open("./questions/all_kana.txt").read()
chars = sorted(list(set(text)))
maxlen = 200 #1問題の最長文字数

print('トータル文字数：', len(text))
print('文字種類数：', len(chars))

questions = []
answers = []
char_num = []

#元問題ファイル読み込み
with open('./questions/moto_kana.txt') as rf:
  lines = rf.readlines()
  for line in lines:
    char_num.append(len(line))
    line = line.split(",")
    line = line[1].replace("\n","")
    questions.append(padding(line, maxlen))
#落とし込み問題ファイル読み込み
with open('./questions/kakunin_kana_one.txt') as rf:
  lines = rf.readlines()
  for line in lines:
    char_num.append(len(line))
    line = line.split(",")
    line = line[1].replace("\n","")
    answers.append(padding(line, maxlen))

print('questions数',len(questions))
print('answers数',len(answers))

#文字とタグ(1,2,3...)を対応付ける、辞書、ハッシュ的な
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

#文字をベクトルに変換(データ数,入力文字数,文字種類数の行列作成)
X = np.zeros((len(questions), maxlen, len(chars)), dtype=np.integer)
Y = np.zeros((len(answers), maxlen, len(chars)), dtype=np.integer)

#one-hot適用
for i in range(len(questions)):
  for t, char in enumerate(questions[i]):
    X[i, t, char_indices[char]] = 1
  for t, char in enumerate(answers[i]):
    Y[i, t, char_indices[char]] = 1

N_train = int(len(questions) * 0.9)
N_validation = len(questions) - N_train
X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, train_size=N_train)

#モデル設定

n_in = len(chars)
n_hidden = 128
n_out = len(chars)

model = Sequential()
#Encoder
#maxlen = 入力データの個数, n_in = データの次元数
model.add(LSTM(n_hidden, input_shape=(maxlen, n_in)))

#Decoder
model.add(RepeatVector(maxlen))
model.add(LSTM(n_hidden, return_sequences=True))

model.add(TimeDistributed(Dense(n_out)))
model.add(Activation('softmax'))

#学習結果読み込み
model.load_weights('./weights.hdf5')

model.compile(loss='categorical_crossentropy',optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999), metrics=['accuracy'])

#モデル保存
json_string = model.to_json()
with open('model.json', 'w') as m:
  m.write(json_string)

#モデル学習

epochs = 3
batch_size = 5

for epoch in range(epochs):
  model.fit(X_train, Y_train, batch_size=batch_size, epochs=1, validation_data=(X_validation, Y_validation))

  index = np.random.randint(0, N_validation)
  question = X_validation[np.array([index])]
  prediction = model.predict_classes(question, verbose=0)

  question = question.argmax(axis=-1)

  q = ''.join(indices_char[i] for i in question[0])
  p = ''.join(indices_char[i] for i in prediction[0])

  print('-' * 15)
  print('元問題：', q.rstrip())
  print('')
  print('落とし込み問題：', p)

#パラメータ保存
model.save_weights('weights.hdf5')


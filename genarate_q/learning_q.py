import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers.core import Dense, Activation, RepeatVector
from keras.layers import LSTM
from keras.layers.wrappers import TimeDistributed
from keras.optimizers import RMSprop
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from keras.models import model_from_json
import random
import sys

path = "./questions/sonneki_kana2.txt"
text = open(path).read().lower()
chars = sorted(list(set(text)))
print(chars)
print('トータル文字数：', len(text))
print('文字種類数：', len(chars))

#文字と数字のタグ付け
char_indices = dict((c,i) for i, c in enumerate(chars))
indices_char = dict((i,c) for i, c in enumerate(chars))

#全時系列データの長さ
length_of_sequences = len(text)
maxlen = 10 #一つの時系列データの長さ

sentences = []
next_char = []

for i in range(0, length_of_sequences - maxlen, 5):
  sentences.append(text[i: i + maxlen])
  next_char.append(text[i + maxlen])

print('データ配列数', len(sentences))

#文字をベクトルに直す
X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.integer)
Y = np.zeros((len(sentences), len(chars)), dtype=np.integer)

#one-hot適用
for i, sentence in enumerate(sentences):
  for t, char in enumerate(sentence):
    X[i, t, char_indices[char]] = 1
  Y[i,char_indices[next_char[i]]] = 1

print(X[4])

#モデル作成

model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(chars))))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))

def sample(preds, temperature=1.0):
  preds = np.asarray(preds).astype('float64')
  preds = np.log(preds) / temperature
  exp_preds = np.exp(preds)
  preds = exp_preds / np.sum(exp_preds)
  probas = np.random.multinomial(1, preds, 1)
  return np.argmax(probas)

for iteration in range(1, 200):
  print('-' * 30)
  print('試行回数：', iteration)
  model.fit(X, Y,
    batch_size=128,
    epochs=1, verbose=2)

  #検証
  #start_index = random.randint(0, len(text) - maxlen -1)
  #sentence = text[start_index: start_index + maxlen]
  #
  sentence = text[104:114]
  generated = sentence
  print('入力文：', sentence)
  next_char = ""
  while next_char != ">":
    x = np.zeros((1, maxlen, len(chars)))
    for t, char in enumerate(sentence):
      x[0, t, char_indices[char]] = 1

    #予測値
    preds = model.predict(x, verbose=0)[0]
    #next_index = np.argmax(preds, axis=-1)
    next_index = sample(preds,1.0)
    #next_char = indices_char[next_index[0]]
    next_char = indices_char[next_index]
    generated += next_char
    sentence = sentence[1:] + next_char

  print('-'*30)
  print('生成した文章')
  print(generated)

model.save_weights('weights.hdf5')

from gensim.models import word2vec
import numpy as np
import matplotlib.pyplot as plt
from keras.layers.core import Dropout
from keras.callbacks import EarlyStopping
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
  return chars.strip() + ' 々' * (maxlen - len(chars.split()))

text = open('./fourChar_data/yozi_wakati_s.txt').read()
chars = sorted(set(text.split()))
maxlen_mean = 59
maxlen_four = 13
four = []
mean = []
vector = 20
flag = True

with open('./fourChar_data/yozi_wakati_s.txt') as rf:
  lines = rf.readlines()
  for line in lines:
    line = line.replace('\n','')
    if flag:
      four.append(padding(line, maxlen_four))
    else:
      mean.append(padding(line, maxlen_mean))
    flag = not(flag)

print('四字熟語数', len(four))
print('意味数', len(mean))



model_w2v = word2vec.Word2Vec.load('./four_char_w2v.model')

X = np.zeros((len(mean),maxlen_mean, vector))
Y = np.zeros((len(four),maxlen_four, vector))
for i in range(len(mean)):
  for t, word in enumerate(four[i].split()):
    Y[i, t] = model_w2v[word]
  for t, word in enumerate(mean[i].split()):
    X[i, t] = model_w2v[word]


N_train = int(len(mean) * 0.9)
N_validation = len(mean) - N_train
X_train, X_validation, Y_train, Y_validation = \
train_test_split(X, Y, train_size=N_train)

n_in = vector
n_hidden = 128
n_out = vector

#early_stopping = EarlyStopping(monitor='val_los', patience=5, verbose=0)

model = Sequential()
#Encoder
model.add(LSTM(n_hidden, input_shape=(maxlen_mean, n_in)))

#Decoder
model.add(RepeatVector(maxlen_four))
model.add(LSTM(n_hidden, return_sequences=True))
model.add(Dropout(0.5))

model.add(TimeDistributed(Dense(n_out)))
model.add(Activation('softmax'))

#学習結果読み込み
#model.laad_weights('./weights_w2v.hdf5')

model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999), \
  metrics=['accuracy'])

'''
モデル保存
json_string = model.to_json()
with open('model.json', 'w') as m:
  m.write(json_string)
'''
#モデル学習
epochs = 2
batch_size = 20

for epoch in range(epochs):
  model.fit(X_train, Y_train, batch_size=batch_size, epochs=1, \
  validation_data=(X_validation, Y_validation))#, callbacks=[early_stopping])

  index = np.random.randint(0, N_validation)
  question = X_validation[np.array([index])]
  prediction = model.predict(question, verbose=0)

  q = ''
  for i in question[0]:
    mean_word = model_w2v.most_similar(positive=[i])
    q += mean_word[0][0]
  print('意味',q)
  p = ''
  for i in prediction[0]:
    pre_word = model_w2v.most_similar(positive=[i])
    p += pre_word[0][0]
  print('予測',p)

import gc; gc.collect()

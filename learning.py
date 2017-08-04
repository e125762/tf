import numpy as np
"""
from keras.models import Sequential
from keras.layers.core import Dense, Activation, RepeatVector
from keras.layers import LSTM
from keras.layers.wrappers import TimeDistributed
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
"""
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
X_train, X_validations, Y_train, Y_validation = train_test_split(X, Y, train_size=N_train)



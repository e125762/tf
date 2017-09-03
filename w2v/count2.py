#分かち書きtxtの形態素解析数(スペースの数)を数える
import numpy as np
flag = True
n_four = []
n_mean = []
count = 1
c = 1
box = []
with open('./fourChar_data/yozi_wakati_s.txt') as f:
  lines = f.readlines()
  for line in lines:
    if flag:
      n_four.append(line.count(' '))
    else:
      n_mean.append(line.count(' '))
      if line.count(' ') > 58:
        box.append(c)
    flag = not(flag)
    c += 1
n_four = np.array(n_four)
n_mean = np.array(n_mean)
print('四字熟語最大長：',np.max(n_four))
print('index：',int(np.argmax(n_four)) * 2 + 1)
print('意味最大長：',np.max(n_mean))
print('index：',int(np.argmax(n_mean)) * 2 + 2)
print('超過index：',box)

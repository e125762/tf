import numpy as np
flag = True
n_four = []
n_mean = []
count = 1
c = 1
box = []
with open('four_char_kana.txt') as f:
  lines = f.readlines()
  for line in lines:
    if flag:
      n_four.append(len(line))
    else:
      n_mean.append(len(line))
      if len(line) > 90:
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

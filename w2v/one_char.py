#四字熟語(かな)一文字ごとにスペースを入れる
flag = True
four_char = ''
file = open('one_char.txt','a')
with open('./yozi_kana.txt') as f:
  lines = f.readlines()
  for line in lines:
    if flag:
      for char in line:
        four_char += char + ' '
      file.write(four_char.rstrip() + '\n')
      four_char = ''
    else:
      file.write(line)
    flag = not(flag)

file.close()


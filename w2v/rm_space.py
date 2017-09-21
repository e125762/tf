#四字熟語(かな)一文字ごとにスペースを入れる
four_char = ''
file = open('./fourChar_data/yozi_wakati_s.txt','a')
with open('./fourChar_data/yozi_wakati.txt') as f:
  lines = f.readlines()
  for line in lines:
    file.write(line.rstrip() + '\n')

file.close()


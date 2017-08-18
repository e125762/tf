#coding: UTF-8
import pykakasi.kakasi as kakasi
import codecs

kakasi = kakasi()
kakasi.setMode('H','H')
kakasi.setMode('K','H')
kakasi.setMode('J','H')
kakasi.setMode('a','a')
conv = kakasi.getConverter()
with open('four_char_kana.txt', 'w') as wf:
  with codecs.open('four_char.txt','r','utf_8') as rf:
    lines = rf.readlines()
    for line in lines:
      reslut = conv.do(line)
      wf.write(reslut)



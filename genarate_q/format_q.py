# -*- coding: utf-8 -*-
import re
with open('./questions/sonneki_data.txt',"w") as wf:
  with open('./questions/sonneki.txt',"r") as rf:
    lines = rf.readlines()
    for line in lines:
      text = re.sub(r'\d+|[一二三四五六七八九十壱弐参拾百千万萬億兆〇]+',"0", line)
      text = '<' + text.replace('\n', '') + '>' + '\n'
      wf.write(text)



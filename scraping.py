import time
from  urllib import request
from bs4 import BeautifulSoup

def repeat_times(page):
  if page is not None:
    page = soup.find('div', {'class': 'pagination'}).find('span')
    return int(page.string[10:])
  else: return 1

def parse(url):
  response = request.urlopen(url)
  html = response.read()
  soup = BeautifulSoup(html, "html.parser")
  return soup

count = 0
mean_count = 0
category = ['a','i','u','e','o','ka','ki','ku','ke','ko','sa','si','su','se','so','ta','ti','tu','te','to','na','ni','nu','ne','no','ha','hi','hu','he','ho','ma','mi','mu','me','mo','ya','yu','yo','ra','ri','ru','re','ro','wa']

mean_f = open('mean.txt', 'a')

with open('four_char.txt','w') as f:
  for mozi in category:
    url = "http://sanabo.com/words/archives/category/{0}".format(mozi)
    soup = parse(url)
    page = soup.find('div', {'class': 'pagination'})
    num = repeat_times(page) #繰り返し回数
    for page_num in range(1, num+1):
      time.sleep(1)
      page_url = 'http://sanabo.com/words/archives/category/{0}/page/{1}'.format(mozi,page_num)
      soup = parse(page_url)
      a_tag = soup.find_all('h3')

      for yozi in a_tag:
        #意味取得部分
        time.sleep(2)
        link = yozi.a['href']
        mean_page = parse(link)
        if mean_page.find('strong') is None:
          continue

        if mean_page.find('strong').string == '意 味：':
          mean_page.find('strong').extract()
          meaning_tag = mean_page.find('li', {'type': 'square'})
          for li_tag in meaning_tag:
            mean_f.write(li_tag.string + '\n')
        else:
          mean_page.span.b.extract()
          meaning_tag = mean_page.find('span', {'class': 's1'})
          for li_tag in meaning_tag:
            mean_f.write(li_tag.string + '\n')
        mean_count += 1

        #四字熟語取得部分
        four_char = yozi.a.string.split('】')[1]
        f.write(four_char + '\n')
        count += 1

print('四字熟語数：',count)
print('四字熟語意味数：',mean_count)
mean_f.close()


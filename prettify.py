from  urllib import request
from bs4 import BeautifulSoup

def parse(url):
  response = request.urlopen(url)
  html = response.read()
  soup = BeautifulSoup(html, "html.parser")
  return soup

url = ''
soup = parse(url)
print(soup.prettify())

 

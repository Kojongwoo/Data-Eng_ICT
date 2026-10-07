import requests
from bs4 import BeautifulSoup

res = requests.get('https://quotes.toscrape.com/', timeout=10)
soup = BeautifulSoup(res.text, 'html.parser')

print(soup.select('div.quotes'))          # 없는 클래스 → 빈 리스트 []
print(soup.select_one('span.txt'))        # 없는 클래스 → None
print(soup.select_one('span.txt').get_text())   # ← 여기서 터집니다


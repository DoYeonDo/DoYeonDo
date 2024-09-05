import re
import requests
from bs4 import BeautifulSoup

def get_total_visitors(blog_url):
    response = requests.get(blog_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # <span class="total"> 태그를 찾음
    total_element = soup.find('span', class_='total')
    
    if total_element:
        # 'Total : ' 텍스트를 제거하고 숫자만 추출
        total_text = total_element.text.strip()
        total_count = total_text.replace('Total : ', '').strip()
        return total_count
    else:
        return "정보 없음"

def update_badge(total_count):
    badge_url = f'https://img.shields.io/badge/Visitors-{total_count}-blue'
    return badge_url

# 방문자 수를 가져옴
total_visitors = get_total_visitors('https://ehduszkdzkd.tistory.com/')

# 배지 URL 생성
badge_url = update_badge(total_visitors)

# README 파일을 업데이트하는 코드 추가
readme_path = 'README.md'

# README.md 파일을 읽고 배지 URL 업데이트
with open(readme_path, 'r', encoding='utf-8') as file:
    readme_content = file.read()

# 기존 배지 URL을 정규 표현식으로 찾아서 새 URL로 업데이트
pattern = re.compile(r'<p align="center">\s*<img src="https://img.shields.io/badge/Visitors-[^\"]+" alt="Visitor Badge">\s*</p>', re.MULTILINE)
updated_content = pattern.sub(f'<p align="center">\n  <img src="{badge_url}" alt="Visitor Badge">\n</p>', readme_content)

# README.md 파일을 업데이트
with open(readme_path, 'w', encoding='utf-8') as file:
    file.write(updated_content)

print(f'배지 URL 업데이트 완료: {badge_url}')

import re
import requests
from bs4 import BeautifulSoup

def get_total_visitors(blog_url):
    response = requests.get(blog_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    total_element = soup.find('span', class_='total')
    
    if total_element:
        total_text = total_element.text.strip()
        total_count = total_text.replace('Total : ', '').replace(',', '').strip()
        return total_count
    else:
        return None

def extract_current_visitor_count(readme_text):
    match = re.search(r'Visitors-(\d+)-blue', readme_text)
    if match:
        return match.group(1)
    return None

def update_badge(total_count):
    return f'https://img.shields.io/badge/Visitors-{total_count}-blue'

readme_path = 'README.md'
blog_url = 'https://ehduszkdzkd.tistory.com/'

# 1. 방문자 수 가져오기
total_visitors = get_total_visitors(blog_url)

# 2. 기존 README.md 읽기
with open(readme_path, 'r', encoding='utf-8') as file:
    readme_content = file.read()

# 3. 기존 방문자 수와 비교
current_count = extract_current_visitor_count(readme_content)

if current_count is None or total_visitors != current_count:
    print(f"방문자 수 변경 감지: {current_count} → {total_visitors}")
    
    # 4. 업데이트 수행
    badge_url = update_badge(total_visitors)
    pattern = re.compile(r'<p align="center">\s*<img src="https://img.shields.io/badge/Visitors-[^\"]+" alt="Visitor Badge">\s*</p>', re.MULTILINE)
    updated_content = pattern.sub(f'<p align="center">\n  <img src="{badge_url}" alt="Visitor Badge">\n</p>', readme_content)

    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)
else:
    print("방문자 수에 변경 없음. README.md 업데이트 생략.")
    exit(0)  # 🚨 변경 없을 경우 GitHub Action에서 실패 방지

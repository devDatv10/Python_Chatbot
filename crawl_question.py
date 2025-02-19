import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}


MAX_PAGES = 5

all_questions = []

for page in range(1, MAX_PAGES + 1):
    url = f"https://voz.vn/f/may-tinh-xach-tay.47/page-{page}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        questions = soup.find_all("a", {"data-tp-primary": "on"})

        for q in questions:
            question_text = q.get_text(strip=True)
            all_questions.append(question_text)

        print(f"Đã lấy dữ liệu từ trang {page}")
    else:
        print(f"Không thể truy cập trang {page}")

with open("voz_questions.txt", "w", encoding="utf-8") as f:
    for idx, question in enumerate(all_questions, 1):
        f.write(f"{idx}. {question}\n")

print(f"Đã lưu {len(all_questions)} câu hỏi vào voz_questions.txt")

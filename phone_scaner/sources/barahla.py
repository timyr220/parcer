import requests
import re
from bs4 import BeautifulSoup

def run():
    print("[🔍] Парсим barahla.net...")
    phone_regex = re.compile(r'\+7\d{10}')
    phones = set()
    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(1, 6):
        url = f"https://barahla.net/bu/realty/page{page}/"
        try:
            r = requests.get(url, timeout=10, headers=headers, verify=False)
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text()
            found = phone_regex.findall(text)
            phones.update(found)
            print(f"[✔] Стр. {page}: найдено {len(found)} номеров")
        except Exception as e:
            print(f"[!] Ошибка на стр. {page}: {e}")

    print(f"[✅] Всего с barahla.net собрано: {len(phones)} номеров\n")
    return phones

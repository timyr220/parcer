import requests
import re
from bs4 import BeautifulSoup

def run():
    print("[🔍] Парсим oirr.ru...")
    phone_regex = re.compile(r'\+7\d{10}')
    phones = set()
    headers = {"User-Agent": "Mozilla/5.0"}
    base_url = "https://oirr.ru/real-estate/"

    for page in range(1, 3):
        try:
            url = f"{base_url}?page={page}"
            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            links = soup.select("a[href^='/real-estate/']")
            ad_links = set([f"https://oirr.ru{a['href']}" for a in links if '/real-estate/' in a['href'] and 'page=' not in a['href']])
            for ad_url in ad_links:
                try:
                    ad_resp = requests.get(ad_url, headers=headers, timeout=10)
                    phones_found = phone_regex.findall(ad_resp.text)
                    if phones_found:
                        phones.update(phones_found)
                        print(f"[+] {ad_url} — найдено {len(phones_found)}")
                except Exception as e:
                    print(f"[!] Ошибка в {ad_url}: {e}")
        except Exception as e:
            print(f"[!] Ошибка на стр. {page}: {e}")

    print(f"[✅] Всего с oirr.ru собрано: {len(phones)} номеров\n")
    return phones

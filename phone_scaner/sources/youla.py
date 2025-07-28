import asyncio, re
from playwright.async_api import async_playwright

# ---------- настройки ----------
START_URL = "https://youla.ru/moskva/uslugi"  # категорию можно менять
MAX_ADS   = 20                                # сколько объявлений парсить
HEADLESS  = True                              # False → видно окно браузера
# --------------------------------

PHONE_RE = re.compile(
    r'(?:tel:)?\+?7[\s‑-]?\(?\d{3}\)?[\s‑-]?\d{3}[\s‑-]?\d{2}[\s‑-]?\d{2}'
)

async def run() -> set[str]:
    print("[🔍] Парсим youla.ru...")
    phones: set[str] = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=HEADLESS,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            locale="ru-RU",
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36")
        )
        page = await context.new_page()

        # открываем список объявлений
        await page.goto(START_URL, wait_until="domcontentloaded", timeout=90000)
        await page.wait_for_selector("a[data-test-id='ad-card-photo-link']", timeout=90000)

        # собираем ссылки на карточки
        cards = await page.locator("a[data-test-id='ad-card-photo-link']").element_handles()
        links = list({
            f"https://youla.ru{await c.get_attribute('href')}"
            for c in cards
        })[:MAX_ADS]

        for link in links:
            try:
                await page.goto(link, timeout=60000)

                # жмём кнопку «Показать телефон»
                btn = page.locator(
                    "button:has-text('Показать'), "
                    "div:has-text('Показать'), "
                    "a:has-text('Показать')"
                )
                if await btn.count():
                    await btn.first.click()
                    await page.wait_for_timeout(1200)

                html = await page.content()
                for raw in PHONE_RE.findall(html):
                    digits = re.sub(r'\D', '', raw)
                    if digits.startswith('8'):
                        digits = '7' + digits[1:]
                    if not digits.startswith('7'):
                        digits = '7' + digits
                    if len(digits) == 11:
                        phones.add(f'+{digits}')
                print(f"[+] {link} — OK")
            except Exception as e:
                print(f"[!] {link} — {e}")

        await browser.close()

    print(f"[✅] С Youla собрали: {len(phones)} номеров")
    return phones

# для одиночного запуска:
if __name__ == "__main__":
    asyncio.run(run())

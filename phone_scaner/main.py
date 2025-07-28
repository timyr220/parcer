from phone_filter import clean_numbers
from sources import youla
import asyncio, os

def save_numbers(phones: set, out="phones.txt"):
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    if not os.path.exists(out):
        open(out, "w").close()
    with open(out, "r+", encoding="utf-8") as f:
        old = set(line.strip() for line in f)
        new = phones - old
        f.writelines(f"{n}\n" for n in sorted(new))
    print(f"[✔] Добавили {len(new)} новых")

all_phones = set()
all_phones.update(clean_numbers(asyncio.run(youla.run())))
save_numbers(all_phones)

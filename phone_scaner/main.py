"""Collect phone numbers from multiple sources and save them to a file."""

import asyncio
import os

from phone_filter import clean_numbers
from sources import barahla, oirr, youla

MAX_NUMBERS = 300  # how many phone numbers we need per run

def save_numbers(phones: set[str], out: str = "phones.txt") -> None:
    """Append new phone numbers to ``out`` while keeping unique values."""

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)

    if not os.path.exists(out):
        open(out, "w").close()

    with open(out, "r+", encoding="utf-8") as f:
        old = set(line.strip() for line in f)
        new = phones - old
        f.writelines(f"{n}\n" for n in sorted(new))

    print(f"[✔] Добавили {len(new)} новых")


def collect_numbers() -> set[str]:
    """Run all sources and combine the results."""

    numbers: set[str] = set()

    # Youla requires Playwright; run it asynchronously
    try:
        numbers.update(clean_numbers(asyncio.run(youla.run())))
    except Exception as e:  # pragma: no cover - network heavy
        print(f"[!] youla.ru error: {e}")

    # The following sources use requests and BeautifulSoup
    for src, name in [(barahla, "barahla.net"), (oirr, "oirr.ru")]:
        try:
            numbers.update(clean_numbers(src.run()))
        except Exception as e:  # pragma: no cover - network heavy
            print(f"[!] {name} error: {e}")

    # limit the amount of numbers to avoid growing infinitely
    return set(sorted(numbers))

def main() -> None:
    numbers = collect_numbers()
    if MAX_NUMBERS:
        numbers = set(list(numbers)[:MAX_NUMBERS])
    save_numbers(numbers)


if __name__ == "__main__":  # pragma: no cover - script entry
    main()

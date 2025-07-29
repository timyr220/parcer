# Phone number parser

This project collects Russian phone numbers from several classifieds websites and saves them to `phones.txt`.

## Usage

Install the required dependencies (Playwright is optional, but without it the Youla source will not work):

```bash
pip install -r phone_scaner/requirements.txt
pip install playwright  # optional for youla.ru
```

If Playwright is installed, you may also need to download browser binaries:

```bash
playwright install chromium
```

Then run the parser:

```bash
python phone_scaner/main.py
```

New phone numbers will be appended to `phone_scaner/phones.txt`.

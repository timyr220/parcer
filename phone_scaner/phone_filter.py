import re

def clean_numbers(raw: set) -> set:
    phone_regex = re.compile(r"\+7\d{10}")
    result = set()
    for num in raw:
        result.update(phone_regex.findall(num))
    return result

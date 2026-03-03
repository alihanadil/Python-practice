import re
import json

def price_change(price_str):
    return float(price_str.replace(" ", "").replace(",", "."))

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

price_patt = r"\d[\d ]*,\d{2}"
all_prices_raw = re.findall(price_patt, text)
all_prices = [price_change(p) for p in all_prices_raw]


product_patt = r"\d+\.\n(.+)"
product = re.findall(product_patt, text)

item_total_patt = r"Стоимость\n([\d ]+,\d{2})"
item_totals_raw = re.findall(item_total_patt, text)
item_totals = [price_change(t) for t in item_totals_raw]

total = sum(item_totals)

datetime_patt = r"Время:\s(\d{2}\.\d{2}\.\d{4})\s(\d{2}:\d{2}:\d{2})"
datetime_match = re.search(datetime_patt, text)

date = datetime_match.group(1) if datetime_match else None
time = datetime_match.group(2) if datetime_match else None


payment_patt = r"(Банковская карта|Наличные)"
payment_match = re.search(payment_patt, text)

payment_method = payment_match.group(1) if payment_match else None

result = {
    "product_names": product,
    "all_prices": all_prices,
    "calculated_total": total,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

print(json.dumps(result, ensure_ascii=False, indent=4))
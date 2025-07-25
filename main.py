import json

# ISO2 коди європейських країн + UA (уточнюй список під свої задачі)
europe_codes = [
    'AL', 'AD', 'AT', 'BY', 'BE', 'BA', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE',
    'FO', 'FI', 'FR', 'DE', 'GI', 'GR', 'VA', 'HU', 'IS', 'IE', 'IT', 'XK', 'LV',
    'LI', 'LT', 'LU', 'MT', 'MD', 'MC', 'ME', 'NL', 'MK', 'NO', 'PL', 'PT', 'RO',
    'RU', 'SM', 'RS', 'SK', 'SI', 'ES', 'SJ', 'SE', 'CH', 'UA', 'GB'
]

# Мапа кодів у повні англійські назви (заповнюй під свої потреби)
country_names = {
    "AL": "Albania",
    "AD": "Andorra",
    "AT": "Austria",
    "BY": "Belarus",
    "BE": "Belgium",
    "BA": "Bosnia and Herzegovina",
    "BG": "Bulgaria",
    "HR": "Croatia",
    "CY": "Cyprus",
    "CZ": "Czechia",
    "DK": "Denmark",
    "EE": "Estonia",
    "FO": "Faroe Islands",
    "FI": "Finland",
    "FR": "France",
    "DE": "Germany",
    "GI": "Gibraltar",
    "GR": "Greece",
    "VA": "Vatican City",
    "HU": "Hungary",
    "IS": "Iceland",
    "IE": "Ireland",
    "IT": "Italy",
    "XK": "Kosovo",
    "LV": "Latvia",
    "LI": "Liechtenstein",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "MT": "Malta",
    "MD": "Moldova",
    "MC": "Monaco",
    "ME": "Montenegro",
    "NL": "Netherlands",
    "MK": "North Macedonia",
    "NO": "Norway",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "RU": "Russia",
    "SM": "San Marino",
    "RS": "Serbia",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "ES": "Spain",
    "SJ": "Svalbard and Jan Mayen",
    "SE": "Sweden",
    "CH": "Switzerland",
    "UA": "Ukraine",
    "GB": "United Kingdom"
}

with open('landing-prices.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

unique = {}

for block in data:
    for country in block['countries']:
        code = country.get('regionCode', '')
        # Тільки потрібні країни
        if code not in europe_codes:
            continue

        name = country.get('regionName') or country_names.get(code, code)
        mini_price = None
        standard_price = None

        for kit in country.get('kits', []):
            desc = kit.get('description', '').lower()
            price = kit.get('price', None)
            if "mini" in desc and mini_price is None:
                mini_price = price
            elif "standard" in desc and standard_price is None:
                standard_price = price

        if code and code not in unique:
            unique[code] = {'name': name, 'mini': mini_price, 'standard': standard_price}

# Генеруємо HTML
rows = [
    f"<tr><td>{data['name']}</td><td>{data['mini'] if data['mini'] is not None else ''}</td><td>{data['standard'] if data['standard'] is not None else ''}</td></tr>"
    for code, data in sorted(unique.items(), key=lambda x: x[1]['name'])
]

html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Starlink Prices — Europe & Ukraine</title>
  <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #181818; color: #eee; margin: 0; padding: 40px; }}
    table {{ border-collapse: collapse; width: 100%; max-width: 800px; margin: auto; background: #23272a; }}
    th, td {{ padding: 10px 14px; border-bottom: 1px solid #36393e; text-align: center; }}
    th {{ background: #23272a; color: #f9d923; font-size: 1.08em; }}
    tr:nth-child(even) {{ background: #202225; }}
    tr:hover {{ background: #292b2f; }}
  </style>
</head>
<body>
  <h1>Starlink Prices (Europe & Ukraine)</h1>
  <table>
    <thead>
      <tr>
        <th>Country</th>
        <th>Mini Price</th>
        <th>Standard Price</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Готово! Файл starlink_prices.html створено.")

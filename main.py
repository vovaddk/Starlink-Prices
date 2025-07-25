import json

# ISO2 коди європейських країн + UA
europe_codes = [
    'AL', 'AD', 'AT', 'BY', 'BE', 'BA', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE',
    'FO', 'FI', 'FR', 'DE', 'GI', 'GR', 'VA', 'HU', 'IS', 'IE', 'IT', 'XK', 'LV',
    'LI', 'LT', 'LU', 'MT', 'MD', 'MC', 'ME', 'NL', 'MK', 'NO', 'PL', 'PT', 'RO',
    'RU', 'SM', 'RS', 'SK', 'SI', 'ES', 'SJ', 'SE', 'CH', 'UA', 'GB'
]

country_names = {
    "AL": "Albania", "AD": "Andorra", "AT": "Austria", "BY": "Belarus",
    "BE": "Belgium", "BA": "Bosnia and Herzegovina", "BG": "Bulgaria",
    "HR": "Croatia", "CY": "Cyprus", "CZ": "Czechia", "DK": "Denmark",
    "EE": "Estonia", "FO": "Faroe Islands", "FI": "Finland", "FR": "France",
    "DE": "Germany", "GI": "Gibraltar", "GR": "Greece", "VA": "Vatican City",
    "HU": "Hungary", "IS": "Iceland", "IE": "Ireland", "IT": "Italy",
    "XK": "Kosovo", "LV": "Latvia", "LI": "Liechtenstein", "LT": "Lithuania",
    "LU": "Luxembourg", "MT": "Malta", "MD": "Moldova", "MC": "Monaco",
    "ME": "Montenegro", "NL": "Netherlands", "MK": "North Macedonia",
    "NO": "Norway", "PL": "Poland", "PT": "Portugal", "RO": "Romania",
    "RU": "Russia", "SM": "San Marino", "RS": "Serbia", "SK": "Slovakia",
    "SI": "Slovenia", "ES": "Spain", "SJ": "Svalbard and Jan Mayen",
    "SE": "Sweden", "CH": "Switzerland", "UA": "Ukraine", "GB": "United Kingdom"
}

# Завантаження JSON-даних
# Примітка: Цей скрипт очікує файл 'landing-prices.json' у тому ж каталозі.
try:
    with open('landing-prices.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
except FileNotFoundError:
    print("Помилка: Файл 'landing-prices.json' не знайдено. Будь ласка, переконайтеся, що він знаходиться в тому ж каталозі, що й цей скрипт.")
    exit()
except json.JSONDecodeError:
    print("Помилка: Не вдалося розібрати 'landing-prices.json'. Переконайтеся, що це дійсний JSON-файл.")
    exit()

unique = {}

for block in json_data:
    for country in block.get('countries', []): # Додано .get() для безпеки
        code = country.get('regionCode', '')
        if code not in europe_codes:
            continue

        name = country.get('regionName') or country_names.get(code, code)
        mini_price = None
        standard_price = None

        for kit in country.get('kits', []): # Додано .get() для безпеки
            desc = kit.get('description', '').lower()
            price = kit.get('price', None)
            if "mini" in desc and mini_price is None:
                mini_price = price
            elif "standard" in desc and standard_price is None:
                standard_price = price

        if code and code not in unique:
            unique[code] = {
                'name': name,
                'mini': mini_price,
                'standard': standard_price
            }

# Формування HTML-рядків для таблиці
rows = [
    f"""<tr>
        <td data-label="Country">{item['name']}</td>
        <td data-label="Mini Price" class="price" data-eur="{item['mini'] if item['mini'] is not None else ''}">{item['mini'] if item['mini'] is not None else ''}</td>
        <td data-label="Standard Price" class="price" data-eur="{item['standard'] if item['standard'] is not None else ''}">{item['standard'] if item['standard'] is not None else ''}</td>
    </tr>"""
    for code, item in sorted(unique.items(), key=lambda x: x[1]['name'])
]

# Основний HTML-код
html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Starlink Prices — Europe & Ukraine</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {{
      font-family: 'Segoe UI', Arial, sans-serif;
      background: #181818;
      color: #eee;
      margin: 0;
      padding: 40px;
    }}
    h1 {{
      text-align: center;
    }}
    .converter {{
      max-width: 800px;
      margin: 20px auto;
      text-align: center;
    }}
    select {{
      padding: 8px;
      font-size: 1em;
      border-radius: 5px;
      background: #23272a;
      color: #eee;
      border: 1px solid #36393e;
    }}
    .error {{
      color: #ff5555;
      font-size: 0.9em;
      margin-top: 10px;
      display: none;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      max-width: 800px;
      margin: auto;
      background: #23272a;
      border-radius: 10px; /* Додано округлення кутів таблиці */
      overflow: hidden; /* Щоб округлення застосовувалося до вмісту */
    }}
    th, td {{
      padding: 10px 14px;
      border-bottom: 1px solid #36393e;
      text-align: center;
    }}
    th {{
      background: #23272a;
      color: #f9d923;
      font-size: 1.08em;
    }}
    tr:nth-child(even) {{ background: #202225; }}
    tr:hover {{ background: #292b2f; }}

    /* --- Адаптивність --- */
    @media (max-width: 600px) {{
      body {{
        padding: 6px;
      }}
      h1 {{
        font-size: 1.22em;
        margin-bottom: 14px;
      }}
      .converter {{
        margin: 10px auto;
      }}
      select {{
        width: 100%;
        max-width: 200px;
      }}
      .error {{
        font-size: 0.8em;
      }}
      table, thead, tbody, th, td, tr {{
        display: block;
        width: 100%;
      }}
      thead {{
        display: none;
      }}
      tr {{
        margin-bottom: 12px;
        background: #23272a;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.14);
        padding: 8px 0 8px 0;
      }}
      td {{
        text-align: left;
        padding: 8px 12px;
        border: none;
        position: relative;
        font-size: 1em;
      }}
      td:before {{
        content: attr(data-label);
        font-weight: bold;
        color: #f9d923;
        display: block;
        margin-bottom: 4px;
      }}
    }}
  </style>
</head>
<body>
  <h1>Starlink Prices (Europe & Ukraine)</h1>
  <div class="converter">
    <label for="currency">Select Currency: </label>
    <select id="currency" onchange="convertCurrency()">
      <option value="EUR">EUR</option>
      <option value="USD">USD</option>
      <option value="GBP">GBP</option>
      <option value="UAH">UAH</option>
      <option value="PLN">PLN</option>
      <option value="CZK">CZK</option>
      <option value="SEK">SEK</option>
      <option value="DKK">DKK</option>
      <option value="NOK">NOK</option>
      <option value="CHF">CHF</option>
    </select>
    <div id="error-message" class="error">Failed to load exchange rates. Using default prices in EUR.</div>
  </div>
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
  <script>
    // Ініціалізація об'єкта для зберігання курсів обміну. Спочатку порожній, курси будуть завантажені з API.
    let exchangeRates = {{}};

    // Асинхронна функція для отримання курсів обміну з API
    async function fetchExchangeRates() {{
      try {{
        // Звернення до API ExchangeRate-API.com
        const response = await fetch('https://v6.exchangerate-api.com/v6/5367321dfae0db753504e8c2/latest/EUR');
        if (!response.ok) {{
          // Обробка помилок HTTP (наприклад, 404, 500)
          throw new Error(`HTTP error! Status: ${{response.status}}, Message: ${{response.statusText}}`);
        }}
        const data = await response.json();
        if (data.result === 'error') {{
          // Обробка помилок, повернутих самим API (наприклад, недійсний ключ)
          throw new Error(`API error: ${{data['error-type']}}`);
        }}
        console.log('API full response:', data); // Логування повної відповіді API для налагодження

        // Ініціалізуємо об'єкт з курсами, встановлюючи EUR як 1
        let fetchedRates = {{ 'EUR': 1 }};

        // !!! ВИПРАВЛЕНО: Змінено data.rates на data.conversion_rates !!!
        if (data.conversion_rates) {{
          fetchedRates['USD'] = data.conversion_rates.USD;
          fetchedRates['GBP'] = data.conversion_rates.GBP;
          fetchedRates['UAH'] = data.conversion_rates.UAH;
          fetchedRates['PLN'] = data.conversion_rates.PLN;
          fetchedRates['CZK'] = data.conversion_rates.CZK;
          fetchedRates['SEK'] = data.conversion_rates.SEK;
          fetchedRates['DKK'] = data.conversion_rates.DKK;
          fetchedRates['NOK'] = data.conversion_rates.NOK;
          fetchedRates['CHF'] = data.conversion_rates.CHF;
        }}

        // Переконуємося, що всі очікувані валюти мають значення,
        // за замовчуванням встановлюємо 1, якщо API не надало курс
        const allCurrencies = ['EUR', 'USD', 'GBP', 'UAH', 'PLN', 'CZK', 'SEK', 'DKK', 'NOK', 'CHF'];
        allCurrencies.forEach(curr => {{
            if (fetchedRates[curr] === undefined) {{
                fetchedRates[curr] = 1; // За замовчуванням 1 (еквівалент EUR)
            }}
        }});

        return fetchedRates;
      }} catch (error) {{
        // Перехоплення будь-яких помилок під час виконання fetch або обробки JSON
        console.error('Error fetching exchange rates:', error.message);
        // Відображення повідомлення про помилку користувачеві
        document.getElementById('error-message').style.display = 'block';
        // У разі помилки повертаємо об'єкт, де всі курси дорівнюють 1 (фактично EUR)
        return {{
          'EUR': 1, 'USD': 1, 'GBP': 1, 'UAH': 1, 'PLN': 1, 'CZK': 1,
          'SEK': 1, 'DKK': 1, 'NOK': 1, 'CHF': 1
        }};
      }}
    }}

    // Функція для конвертації та відображення цін
    async function convertCurrency() {{
      const currency = document.getElementById('currency').value;
      // Очікування отримання актуальних курсів обміну
      exchangeRates = await fetchExchangeRates();
      console.log('Using exchange rates:', exchangeRates); // Логування курсів, які використовуються

      const rate = exchangeRates[currency]; // Отримання курсу для обраної валюти
      const prices = document.querySelectorAll('.price'); // Вибір усіх елементів з класом 'price'

      // Приховуємо повідомлення про помилку на початку кожної спроби конвертації
      document.getElementById('error-message').style.display = 'none';

      prices.forEach(cell => {{
        const eurPrice = cell.getAttribute('data-eur'); // Отримання оригінальної ціни в EUR
        const parsedEurPrice = parseFloat(eurPrice);

        if (eurPrice && !isNaN(parsedEurPrice)) {{ // Перевірка, чи існує оригінальна ціна в EUR і чи є вона числом
          // Оскільки 'rate' тепер завжди визначений (або з API, або 1), можемо конвертувати безпосередньо
          // ВИПРАВЛЕНО: Використання parseFloat для видалення зайвих нулів
          const convertedPrice = (parsedEurPrice * rate).toFixed(2);
          cell.textContent = `${{convertedPrice}} ${{currency}}`; // Оновлення тексту комірки
        }} else {{
          // Якщо оригінальної ціни в EUR немає, залишаємо комірку порожньою
          cell.textContent = '';
        }}
      }});
    }}

    // Викликати конвертацію при завантаженні сторінки, щоб відобразити ціни з самого початку
    convertCurrency();
  </script>
</body>
</html>
"""

# Запис згенерованого HTML у файл index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Готово! Файл index.html створено з валідним API-ключем і виправленням змінної.")

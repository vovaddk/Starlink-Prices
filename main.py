import json
import requests

# ISO2 коди європейських країн + UA
europe_codes = [
    'AL', 'AD', 'AT', 'BY', 'BE', 'BA', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE',
    'FO', 'FI', 'FR', 'DE', 'GI', 'GR', 'VA', 'HU', 'IS', 'IE', 'IT', 'XK', 'LV',
    'LI', 'LT', 'LU', 'MT', 'MD', 'MC', 'ME', 'NL', 'MK', 'NO', 'PL', 'PT', 'RO',
    'RU', 'SM', 'RS', 'SK', 'SI', 'ES', 'SJ', 'SE', 'CH', 'UA', 'GB'
]

country_names = {
    "AL": "Albania", "AT": "Austria", "BE": "Belgium", "BG": "Bulgaria",
    "HR": "Croatia", "CY": "Cyprus", "CZ": "Czechia", "DK": "Denmark",
    "EE": "Estonia", "FO": "Faroe Islands", "FI": "Finland", "FR": "France",
    "DE": "Germany", "GR": "Greece", "HU": "Hungary", "IS": "Iceland", "IE": "Ireland", "IT": "Italy",
    "XK": "Kosovo", "LV": "Latvia", "LI": "Liechtenstein", "LT": "Lithuania",
    "LU": "Luxembourg", "MT": "Malta", "MD": "Moldova",
    "NL": "Netherlands", "MK": "North Macedonia",
    "NO": "Norway", "PL": "Poland", "PT": "Portugal", "RO": "Romania",
     "SK": "Slovakia",
    "SI": "Slovenia", "ES": "Spain", "SJ": "Svalbard and Jan Mayen",
    "SE": "Sweden", "CH": "Switzerland", "UA": "Ukraine", "GB": "United Kingdom"
}

# Мапування коду країни на код валюти
country_to_currency = {
    "AL": "ALL", "AZ": "AZN", "BG": "BGN", "CH": "CHF", "CZ": "CZK",
    "DK": "DKK","FO": "DKK", "GB": "GBP", "HU": "HUF","IS":"ISK", "MD": "MDL","MK":"MKD", "NO": "NOK", "PL": "PLN", "RO": "RON","SJ":"NOK", "SE": "SEK", "UA": "USD"
}

# Країни Єврозони (використовують EUR)
euro_zone_countries = [
    'AT', 'BE', 'CY', 'EE', 'FI', 'FR', 'DE', 'GR', 'IE', 'IT', 'LV', 'LT',
    'LU', 'MT', 'NL', 'PT', 'SK', 'SI', 'XK'
]

for code in euro_zone_countries:
    if code not in country_to_currency:
        country_to_currency[code] = 'EUR'

# Завантаження JSON-даних
try:
    with open('landing-prices.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
except FileNotFoundError:
    print("Помилка: Файл 'landing-prices.json' не знайдено.")
    exit()
except json.JSONDecodeError:
    print("Помилка: Не вдалося розібрати 'landing-prices.json'.")
    exit()

# --- Отримання курсів валют ---
exchange_rates = {}
API_KEY = "5367321dfae0db753504e8c2" # Ваш API-ключ
BASE_CURRENCY = "EUR"

try:
    response = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{BASE_CURRENCY}")
    response.raise_for_status()
    data = response.json()
    if data['result'] == 'success':
        exchange_rates = data['conversion_rates']
        exchange_rates['EUR'] = 1.0
        print("Курси валют успішно завантажено.")
    else:
        print(f"Помилка API: {data.get('error-type', 'Невідома помилка')}")
except Exception as e:
    print(f"Помилка запиту до API: {e}")

# Обробка даних
unique = {}
for block in json_data:
    for country in block.get('countries', []):
        code = country.get('regionCode', '')
        if code not in europe_codes:
            continue

        name = country.get('regionName') or country_names.get(code, code)
        mini_price_eur = None
        standard_price_eur = None
        
        original_currency = country_to_currency.get(code, 'EUR')

        for kit in country.get('kits', []):
            desc = kit.get('description', '').lower()
            price = kit.get('price', None)
            
            if price is not None:
                price_in_eur = price
                if original_currency != 'EUR' and original_currency in exchange_rates:
                    rate = exchange_rates.get(original_currency, 0)
                    if rate != 0:
                        price_in_eur = round(price / rate, 2)
            else:
                price_in_eur = None

            if "mini" in desc and mini_price_eur is None:
                mini_price_eur = price_in_eur
            elif "standard" in desc and standard_price_eur is None:
                standard_price_eur = price_in_eur

        if code and code not in unique:
            unique[code] = {
                'name': name,
                'mini': mini_price_eur,
                'standard': standard_price_eur
            }

# Початкове сортування за алфавітом
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
      padding: 20px; 
    }}
    
    h1 {{ 
      text-align: center; 
      margin: 20px 0; 
      font-size: 1.8em; 
    }}
    
    .controls {{ 
      background: #23272a; 
      border-radius: 10px; 
      padding: 20px; 
      margin: 20px auto; 
      max-width: 800px; 
      box-shadow: 0 4px 12px rgba(0,0,0,0.3); 
    }}
    
    .control-row {{ 
      display: flex; 
      flex-wrap: wrap; 
      gap: 20px; 
      align-items: center; 
      justify-content: center; 
      margin-bottom: 15px; 
    }}
    
    .control-row:last-child {{ 
      margin-bottom: 0; 
    }}
    
    .control-group {{ 
      display: flex; 
      flex-direction: column; 
      align-items: center; 
      min-width: 160px; 
    }}
    
    .control-group label {{ 
      color: #f9d923; 
      font-weight: bold; 
      margin-bottom: 8px; 
      font-size: 0.95em; 
    }}
    
    input[type="text"], select {{ 
      padding: 12px; 
      font-size: 1em; 
      border-radius: 8px; 
      background: #2c2f33; 
      color: #eee; 
      border: 2px solid #36393e; 
      width: 100%; 
      max-width: 160px; 
      transition: border-color 0.3s ease; 
    }}
    
    input[type="text"]:focus, select:focus {{ 
      outline: none; 
      border-color: #f9d923; 
    }}
    
    .error {{ 
      color: #ff5555; 
      font-size: 0.9em; 
      text-align: center; 
      margin-top: 15px; 
      display: none; 
      padding: 10px; 
      background: rgba(255, 85, 85, 0.1); 
      border-radius: 8px; 
    }}
    
    table {{ 
      border-collapse: collapse; 
      width: 100%; 
      max-width: 800px; 
      margin: 20px auto; 
      background: #23272a; 
      border-radius: 10px; 
      overflow: hidden; 
      box-shadow: 0 4px 12px rgba(0,0,0,0.3); 
    }}
    
    th, td {{ 
      padding: 12px 16px; 
      border-bottom: 1px solid #36393e; 
      text-align: left; 
    }}
    
    th {{ 
      background: #2c2f33; 
      color: #f9d923; 
      font-size: 1.1em; 
      cursor: pointer; 
      user-select: none; 
      transition: background-color 0.3s ease; 
    }}
    
    th:hover {{ 
      background: #36393e; 
    }}
    
    td:first-child, th:first-child {{ 
      text-align: left; 
    }}
    
    td.price, th.price-header {{ 
      text-align: right; 
    }}
    
    tr:nth-child(even) {{ 
      background: #202225; 
    }}
    
    tr:hover {{ 
      background: #292b2f; 
    }}

    /* Мобільні стилі */
    @media (max-width: 768px) {{
      body {{ 
        padding: 15px; 
      }}
      
      h1 {{ 
        font-size: 1.5em; 
        margin: 15px 0; 
      }}
      
      .controls {{ 
        padding: 15px; 
        margin: 15px auto; 
      }}
      
      .control-row {{ 
        flex-direction: column; 
        gap: 15px; 
        align-items: stretch; 
      }}
      
      .control-group {{ 
         
        min-width: unset; 
        
      }}
      
      input[type="text"], select {{ 
         
        padding: 14px; 
      }}
      
      table, thead, tbody, th, td, tr {{ 
        display: block; 
        width: 100%; 
      }}
      
      thead {{ 
        display: none; 
      }}
      
      tr {{ 
        margin-bottom: 15px; 
        background: #23272a; 
        border-radius: 10px; 
        box-shadow: 0 3px 8px rgba(0,0,0,0.2); 
        padding: 15px; 
        border: none; 
      }}
      
      td {{ 
        text-align: right; 
        padding: 8px 0; 
        border: none; 
        position: relative; 
        font-size: 1em; 
        display: flex; 
        align-items: center; 
        border-bottom: 1px solid #36393e; 
      }}
      
      td:last-child {{ 
        border-bottom: none; 
      }}
      
      td:before {{ 
        content: attr(data-label); 
        font-weight: bold; 
        color: #f9d923; 
        text-align: left; 
        padding-right: 10px; 
        min-width: 120px; 
      }}
    }}
    
    @media (max-width: 480px) {{
      body {{ 
        padding: 10px; 
      }}
      
      .controls {{ 
        padding: 12px; 
      }}
      
      h1 {{ 
        font-size: 1.3em; 
      }}
    }}
  </style>
</head>
<body>
  <h1>Starlink Prices (Europe & Ukraine)</h1>
  
  <div class="controls">
    <div class="control-row">
      <div class="control-group">
        <label for="searchInput">Search Country</label>
        <input type="text" id="searchInput" onkeyup="searchCountry()" placeholder="Enter country name...">
      </div>
      <div class="control-group">
        <label for="currency">Select Currency</label>
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
      </div>
      <div class="control-group">
        <label for="miniSort">Sort Mini</label>
        <select id="miniSort" onchange="applySorting()">
          <option value="none">No sorting</option>
          <option value="asc">Cheapest first</option>
          <option value="desc">Most expensive first</option>
        </select>
      </div>
      <div class="control-group">
        <label for="standardSort">Sort Standard</label>
        <select id="standardSort" onchange="applySorting()">
          <option value="none">No sorting</option>
          <option value="asc">Cheapest first</option>
          <option value="desc">Most expensive first</option>
        </select>
      </div>
    </div>
    <div id="error-message" class="error">Failed to load exchange rates. Using default prices in EUR.</div>
  </div>
  
  <table id="pricesTable">
    <thead>
      <tr>
        <th onclick="sortTable(0)">Country</th>
        <th onclick="sortTable(1)" class="price-header">Mini Price</th>
        <th onclick="sortTable(2)" class="price-header">Standard Price</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
  
  <script>
    let exchangeRates = {{}};
    let sortState = {{ column: 0, direction: 'asc' }};

    async function fetchExchangeRates() {{
      try {{
        const response = await fetch('https://v6.exchangerate-api.com/v6/{API_KEY}/latest/EUR');
        if (!response.ok) throw new Error(`HTTP error! Status: ${{response.status}}`);
        const data = await response.json();
        if (data.result === 'error') throw new Error(`API error: ${{data['error-type']}}`);
        exchangeRates = data.conversion_rates;
        exchangeRates['EUR'] = 1.0;
        return exchangeRates;
      }} catch (error) {{
        console.error('Error fetching exchange rates:', error.message);
        document.getElementById('error-message').style.display = 'block';
        return {{ 'EUR': 1, 'USD': 1, 'GBP': 1, 'UAH': 1, 'PLN': 1, 'CZK': 1, 'SEK': 1, 'DKK': 1, 'NOK': 1, 'CHF': 1 }};
      }}
    }}

    async function convertCurrency() {{
      if (Object.keys(exchangeRates).length === 0) {{
         await fetchExchangeRates();
      }}
      const currency = document.getElementById('currency').value;
      const rate = exchangeRates[currency] || 1;
      document.querySelectorAll('.price').forEach(cell => {{
        const eurPrice = cell.getAttribute('data-eur');
        if (eurPrice && !isNaN(parseFloat(eurPrice))) {{
          const convertedPrice = (parseFloat(eurPrice) * rate).toFixed(2);
          cell.textContent = `${{convertedPrice}} ${{currency}}`;
        }} else {{
          cell.textContent = 'N/A';
        }}
      }});
    }}

    function searchCountry() {{
        const input = document.getElementById("searchInput");
        const filter = input.value.toUpperCase();
        const tbody = document.getElementById("pricesTable").getElementsByTagName("tbody")[0];
        const rows = tbody.getElementsByTagName("tr");

        for (let i = 0; i < rows.length; i++) {{
            const countryCell = rows[i].getElementsByTagName("td")[0];
            if (countryCell) {{
                const txtValue = countryCell.textContent || countryCell.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {{
                    rows[i].style.display = "";
                }} else {{
                    rows[i].style.display = "none";
                }}
            }}
        }}
    }}

    function applySorting() {{
        const miniSort = document.getElementById("miniSort").value;
        const standardSort = document.getElementById("standardSort").value;
        
        // Якщо обидва фільтри вимкнені, повертаємо до алфавітного сортування
        if (miniSort === 'none' && standardSort === 'none') {{
            sortTable(0); // Сортування за країною
            return;
        }}
        
        const table = document.getElementById("pricesTable");
        const tbody = table.tBodies[0];
        const rows = Array.from(tbody.rows);
        
        rows.sort((a, b) => {{
            let comparison = 0;
            
            // Спочатку сортуємо за Mini, якщо вибрано
            if (miniSort !== 'none') {{
                const miniA = parseFloat(a.cells[1].dataset.eur) || -1;
                const miniB = parseFloat(b.cells[1].dataset.eur) || -1;
                
                if (miniA !== miniB) {{
                    comparison = miniA > miniB ? 1 : -1;
                    return miniSort === 'asc' ? comparison : comparison * -1;
                }}
            }}
            
            // Потім сортуємо за Standard, якщо вибрано
            if (standardSort !== 'none') {{
                const standardA = parseFloat(a.cells[2].dataset.eur) || -1;
                const standardB = parseFloat(b.cells[2].dataset.eur) || -1;
                
                if (standardA !== standardB) {{
                    comparison = standardA > standardB ? 1 : -1;
                    return standardSort === 'asc' ? comparison : comparison * -1;
                }}
            }}
            
            // Якщо ціни однакові, сортуємо за назвою країни
            const nameA = a.cells[0].textContent.trim();
            const nameB = b.cells[0].textContent.trim();
            
            return nameA.localeCompare(nameB);
        }});
        
        // Очищуємо та заново додаємо відсортовані рядки
        while (tbody.firstChild) {{
            tbody.removeChild(tbody.firstChild);
        }}
        rows.forEach(row => tbody.appendChild(row));
        
        // Скидаємо стан сортування таблиці
        sortState = {{ column: -1, direction: 'asc' }};
    }}

    function sortTable(columnIndex) {{
        const table = document.getElementById("pricesTable");
        const tbody = table.tBodies[0];
        const rows = Array.from(tbody.rows);
        const isNumeric = columnIndex > 0;

        let direction = 'asc';
        if (sortState.column === columnIndex && sortState.direction === 'asc') {{
            direction = 'desc';
        }}
        
        sortState = {{ column: columnIndex, direction: direction }};

        rows.sort((a, b) => {{
            const cellA = a.cells[columnIndex];
            const cellB = b.cells[columnIndex];

            let valA, valB;

            if (isNumeric) {{
                valA = parseFloat(cellA.dataset.eur) || -1;
                valB = parseFloat(cellB.dataset.eur) || -1;
            }} else {{
                valA = cellA.textContent.trim();
                valB = cellB.textContent.trim();
            }}
            
            let comparison = 0;
            if (valA > valB) {{
                comparison = 1;
            }} else if (valA < valB) {{
                comparison = -1;
            }}

            return direction === 'asc' ? comparison : comparison * -1;
        }});

        while (tbody.firstChild) {{
            tbody.removeChild(tbody.firstChild);
        }}
        rows.forEach(row => tbody.appendChild(row));
    }}

    document.addEventListener('DOMContentLoaded', convertCurrency);
  </script>
</body>
</html>
"""

# Запис згенерованого HTML у файл index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Готово! Файл index.html створено з покращеними фільтрами для мобільних пристроїв.")
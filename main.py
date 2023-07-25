import requests
from bs4 import BeautifulSoup
import pandas as pd

OUTPUT_FILE = 'trade.csv'
TO_CSV = True
DISPLAY_DATA = True

URL_HEADER = 'https://www.settrade.com'
URL = f'{URL_HEADER}/th/equities/market-summary/overview'


trades = set()
clean_data = []

req = requests.get(URL)
soup = BeautifulSoup(req.content, 'html.parser')
divs = soup.find_all('div', {'class': 'table-responsive'})[-1]

if divs:
    rows = divs.find_all('tr')[1:]

    for row in rows:
        cols = row.find_all('td')[:-1]
        data = [col.get_text().strip() for col in cols]
        low, high = data[4].split()
        unit, percentage = data[2].split()
        percentage = percentage[1:-2]
        data = data[:4] + [low, high] + data[5:]
        data = data[:2] + [unit, percentage] + data[3:]
        clean_data.append(data)

columns = ['Stock', 'Latest Price', 'Change by Unit', 'Change by Percentage', 'Opening Price', 'Intraday Low', 'Intraday High', 'Volume', 'Value']
database = pd.DataFrame(clean_data, columns=columns)

if TO_CSV:
    database.to_csv(OUTPUT_FILE, index=False)

if DISPLAY_DATA:
    print(database)

if __name__ == '__main__':
    print('\nDone')

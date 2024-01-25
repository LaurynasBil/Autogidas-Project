import requests
from bs4 import BeautifulSoup
import pandas as pd


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
    }

data = []
for i in range(1, 245):
    url=f'https://autogidas.lt/skelbimai/automobiliai/?f_50=kaina_asc&page={i}'

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', class_='article-item')

    new_posting_list = []

    for item in items:
        if item:
            if item.find('h2', class_='item-title'):
                name = item.find('h2', class_='item-title').text.strip()
                year = item.find('span', class_='icon param-year').text.strip().replace('Metai\n', '')
                fuel_type = item.find('span', class_='icon param-fuel-type').text.strip().replace('Kuro tipas\n', '')
                if item.find('span', class_='icon param-mileage'):
                    mileage = item.find('span', class_='icon param-mileage').text.strip().replace('Rida\n', '')
                else:
                    mileage = None
                if item.find('span', class_='icon param-gearbox'):
                    gearbox = item.find('span', class_='icon param-gearbox').text.strip().replace('Pavarų dėžė\n', '')
                else:
                    gearbox = None
                if item.find('span', class_='icon param-engine'):
                    engine = item.find('span', class_='icon param-engine').text.strip().replace('Variklis\n', '').split()[0]
                    if len(item.find('span', class_='icon param-engine').text.strip().replace('Variklis\n',
                                                                                              '').split()) >= 3:
                        power = \
                        item.find('span', class_='icon param-engine').text.strip().replace('Variklis\n', '').split()[2]
                    else:
                        power = None
                else:
                    engine = None
                    power = None
                if item.find('span', class_='icon param-location'):
                    location = item.find('span', class_='icon param-location').text.strip().replace('Miestas\n', '')
                else:
                    location = None
                price = item.find('div', class_='item-price').text.strip()
            else:
                continue
        else:
            continue
        new_posting_list.append({
            'Name': name,
            'Made': year,
            'Fuel Type': fuel_type,
            'Mileage': mileage,
            'Gearbox': gearbox,
            'Engine': engine,
            'Power' : power,
            'Location': location,
            'Price': price
        })
    for skelbimas in new_posting_list:
        data.append(skelbimas)
df = pd.DataFrame(data)
df.to_csv("files/autogidaslistings.csv", index = False)
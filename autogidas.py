# Importing the 'requests' library for making HTTP requests
import requests
# Importing the 'BeautifulSoup' class from the 'bs4' (Beautiful Soup) library for pulling data out
from bs4 import BeautifulSoup
# Importing the 'pandas' library and aliasing it as 'pd' for working with data in a tabular format
import pandas as pd


# Defining headers to mimic a user agent, which can be useful when making web requests to prevent being blocked
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
    }

# Creating an empty list to store data
data = []
# Iterating through pages (from 1 to 246) on autogidas.lt website to scrape data
for i in range(1, 247):
    # Constructing the URL for each page
    url=f'https://autogidas.lt/skelbimai/automobiliai/?f_50=kaina_asc&page={i}'

    # Sending an HTTP GET request to the specified URL with custom headers
    response = requests.get(url, headers=headers)

    # Parsing the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extracting all elements with the specified HTML class from the parsed HTML content
    items = soup.find_all('div', class_='article-item')

    # Creating an empty list to store data for the current page
    new_posting_list = []

    # Iterating through each item on the page
    for item in items:
        # Checking if the 'item' exists
        if item:
            # Checking if the item containing a 'h2' tag with class 'item-title' for the car exists
            if item.find('h2', class_='item-title'):
                # Extracting and cleaning the 'name' attribute by finding 'h2' tag with the 'item-title' class
                name = item.find('h2', class_='item-title').text.strip()
                # Extracting and cleaning the 'year' attribute, replacing the word 'Metai' (Years) with an empty string to get the year in YYYY-MM format
                year = item.find('span', class_='icon param-year').text.strip().replace('Metai\n', '')
                # Extracting and cleaning the 'fuel_type' attribute, replacing the words 'Kuro tipas' (Fuel type) with an empty string to get only the fuel type names
                fuel_type = item.find('span', class_='icon param-fuel-type').text.strip().replace('Kuro tipas\n', '')
                # Extracting and cleaning the 'mileage' attribute by replacing the word 'Rida' (Mileage) with an empty string to only get the mileage if available, otherwise setting it to None
                mileage = item.find('span', class_='icon param-mileage').text.strip().replace('Rida\n', '') if item.find('span', class_='icon param-mileage') else None
                # Extracting and cleaning the 'gearbox' attribute if available, otherwise setting it to None
                gearbox = item.find('span', class_='icon param-gearbox').text.strip().replace('Pavarų dėžė\n', '') if item.find('span', class_='icon param-gearbox') else None
                 # Extracting and cleaning the 'engine' and 'power' attributes by splitting them from one class atribute if available, otherwise setting them to None
                if item.find('span', class_='icon param-engine'):
                    engine = item.find('span', class_='icon param-engine').text.strip().replace('Variklis\n', '').split()[0]
                    # Checking to see if there are more or equal amount of elements from the split to 3 in order to get the 'power' atribute otherwise setting to None
                    power = item.find('span', class_='icon param-engine').text.strip().replace('Variklis\n', '').split()[2] if len(item.find('span', class_='icon param-engine').text.strip().replace('Variklis\n', '').split()) >= 3 else None
                else:
                    engine = None
                    power = None
                # Extracting and cleaning the 'location' attribute if available, otherwise setting it to None
                location = item.find('span', class_='icon param-location').text.strip().replace('Miestas\n', '') if item.find('span', class_='icon param-location') else None
                # Extracting and cleaning the 'price' attribute
                price = item.find('div', class_='item-price').text.strip()
            else:
                # Continue to the next iteration if the item containing a 'h2' tag with class 'item-title' for the car does not exist
                continue
        else:
            # Continue to the next iteration if 'item' does not exist
            continue

        # Adding the extracted attributes to 'new_posting_list' as a dictionary
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

    # Appending the data from 'new_posting_list' to the main 'data' list
    for listing in new_posting_list:
        data.append(listing)

# Creating a DataFrame from the 'data' list
df = pd.DataFrame(data)
# Saving the DataFrame to a CSV file without including the index for faster data reach and to ensure we have a back up for working with the DataFrame
df.to_csv("files/autogidaslistings.csv", index=False)

# Reading the CSV file into a new DataFrame
df = pd.read_csv('files/autogidaslistings.csv')

# Extracting 'Make' and 'Model' from the 'Name' column and rearranging the DataFrame columns
df['Make'] = df['Name'].str.split(' ', expand=True)[0]
df['Model'] = df['Name'].str.split(' ', expand=True)[1]
cols = df.columns.tolist()
cols = cols[-2:] + cols[:-2]
df = df[cols]

# Cleaning and transforming columns 'Price', 'Mileage' and 'Fuel type'
df['Price'] = df['Price'].str.replace(' €', '').str.replace(' ', '').str.replace('+mokesčiai', '').astype('int')
df['Mileage'] = df['Mileage'].str.replace(' km', '').str.replace(' ', '').astype('float')
df['Fuel Type'] = df['Fuel Type'].str.replace(' ', '').str.replace('Gamtinėsdujos', 'Dujos')
# Filling empty 'Gearbox' column spots with 'Automatinė' (Automatic) because the only cars that don't have those parameters are electric and they are all automatic
df['Gearbox'] = df['Gearbox'].fillna('Automatinė')
# Cleaning columns 'Engine' and 'Mileage' for user errors in the postings
df['Engine'] = df['Engine'].apply(lambda x: x / 10 if x > 10 else x)
df['Mileage'] = df['Mileage'].apply(lambda x: x / 10 if x > 2000000 and x % 10 == 0 else x)
# Replacing 'Naujas' (New) in the 'Made' column with '2024-01' for the current year and month
df['Made'] = df['Made'].str.replace('Naujas', '2024-01')
# Extracting the 'Year' from the modified 'Made' column and converting it to an integer
df['Year'] = df['Made'].str.split('-', expand=True)[0].astype('int')

# Saving the final DataFrame to an Excel file with a specified sheet name
df.to_excel('files/autogidas_listings_final.xlsx', sheet_name='Data')
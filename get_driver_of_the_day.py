import requests
from bs4 import BeautifulSoup
import json

url = "https://racingnews365.com/f1-driver-of-the-day"

response = requests.get(url)

output_data = []  # List to store rows

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', class_='table-default table-default--expanded content-field__table')

    if table:
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if columns and 'Cancelled' not in [column.text.strip() for column in columns]:
                output_data.append([column.text.strip() for column in columns])
    else:
        print("Table not found on the page.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Dump the entire list to the JSON file
with open("driver_of_the_day.json", "w") as output_file:
    json.dump(output_data, output_file, indent=2)

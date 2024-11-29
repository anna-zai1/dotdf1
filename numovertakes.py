import requests
import pandas as pd
from bs4 import BeautifulSoup

race_url = "https://racingpass.net/2023-italian-gp-overtakes/"

driver_of_the_day = "sainz"

response = requests.get(race_url)

if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div with the specified class
    target_div = soup.find('div', class_='wp-block-group is-layout-flow wp-container-core-group-layout-7 wp-block-group-is-layout-flow')

    # Check if the div was found
    if target_div:
        # Find the table inside the div
        table = target_div.find('table', {'id': 'tablepress-754', 'class': 'tablepress tablepress-id-754'})

        # Check if the table was found
        if table:
            # Count the number of overtakes for the "Driver of the Day"
            overtakes_count = 0

            for row in table.find_all('tr'):
                columns = row.find_all('td')

                # Check if there are at least three columns in the row
                if len(columns) >= 3:
                    # Extract the text content of the third column
                    third_column_data = columns[2].text.strip().lower()

                    # Check if the "Driver of the Day" name appears in the third column
                    if driver_of_the_day.lower() in third_column_data:
                        overtakes_count += 1

            # Print the overtakes count
            print(f"Overtakes count for {driver_of_the_day} in Italy: {overtakes_count}")
        else:
            print("No table found for Italy race.")
    else:
        print("No div with the specified class found.")
else:
    print(f"Failed to retrieve the page for Italy race. Status code: {response.status_code}")

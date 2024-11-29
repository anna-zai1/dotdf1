import pandas as pd
import requests
from bs4 import BeautifulSoup

file_path = 'race_stories_final_2023.csv' 
df = pd.read_csv(file_path)

url = 'https://www.skysports.com/f1/news/12433/12790328/dhl-fastest-lap-award-2023'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    widget_container_div = soup.find('div', class_='article__widge-container')

    if widget_container_div:
        widget_table_div = widget_container_div.find('div', class_='widge-table')

        if widget_table_div:
            table_body_div = widget_table_div.find('div', class_='widget-table__body')

            if table_body_div:
                new_column_data = [td.text.strip() for td in table_body_div.select('tbody tr td:nth-child(2)')]

                df['NewScrapedColumn'] = new_column_data

                output_file_path = 'racestory_fastestlap.csv'
                df.to_csv(output_file_path, index=False)

                print(df)

            else:
                print("Table body div not found. Check the HTML structure.")
        else:
            print("Widget table div not found. Check the HTML structure.")
    else:
        print("Widget container div not found. Check the HTML structure.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

import requests
import csv
import json

with open('driver_of_the_day.json', 'r') as json_file:
    drivers_of_the_day = json.load(json_file)

csv_file_path = 'driver_results_2023_ergast.csv'
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(['Race', 'Driver', 'Start Position', 'End Position'])

    for race_info in drivers_of_the_day:
        race_name, driver_full_name = race_info
        country_name = race_name.split(' ', 1)[0]
        race_name = f"{country_name} Grand Prix"

        driver_last_name = driver_full_name.split()[-1].lower()

        ergast_url = f"https://ergast.com/api/f1/2023/drivers/{driver_last_name}/results.json"

        response = requests.get(ergast_url)

        if response.status_code == 200:
            try:
                driver_results = response.json()['MRData']['RaceTable']['Races']

                race_result = next((result for result in driver_results if result['raceName'] == race_name), None)

                if race_result:
                    driver_id = race_result['Results'][0]['Driver']['driverId']
                    start_position = race_result['Results'][0]['grid']
                    end_position = race_result['Results'][0]['position']
                    csv_writer.writerow([race_name, driver_id, start_position, end_position])
                else:
                    print(f"Race not found for {race_name} in the results of {driver_last_name}")
            except json.decoder.JSONDecodeError:
                print(f"Error decoding JSON for {race_name} - {driver_last_name}")
        else:
            print(f"Error in API request for {driver_last_name}. Status code: {response.status_code}")

print(f"Data has been saved to {csv_file_path}")

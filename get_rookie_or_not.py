import pandas as pd

file_path = 'race_stories_final_2023.csv' 
df = pd.read_csv(file_path)

rookie_drivers = ["piastri", "sargeant", "de vries"]
df['Rookie?'] = df['Driver'].isin(rookie_drivers)

output_file_path = 'race_stories_rookies_final_2023.csv'
df.to_csv(output_file_path, index=False)

print(df)

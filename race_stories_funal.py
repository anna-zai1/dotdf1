import pandas as pd

file_path = 'driver_results_2023_ergast.csv' 
df = pd.read_csv(file_path)

df['Race Story'] = (df['Start Position'] - df['End Position']).astype(int)

output_file_path = 'race_stories_final_2023.csv'
df.to_csv(output_file_path, index=False)

print(df)

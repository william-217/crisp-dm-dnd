import pandas as pd
import os

# Adjust the path to match your folder
df = pd.read_csv('./data/dnd_dataset.csv')

df.drop(columns=['Unnamed: 0', 'char_id'], inplace=True)

# --- Step 1: Sanitize Data ---
stat_columns = ['base_hp', 'stats_1', 'stats_2', 'stats_3', 'stats_4', 'stats_5', 'stats_6']
df = df[(df[stat_columns] != 0).all(axis=1)]

# --- Step 1.1: Use Webscraping to get all allowed races and classes from https://www.dndbeyond.com/species and https://www.dndbeyond.com/classes


# --- Step 1.2: Update the dataset to filter this out

unique_races = df['race'].dropna().unique()
unique_races.sort()

race_counts = df['race'].value_counts()

with open('unique_races.txt', 'w', encoding='utf-8') as f:
    for race, count in race_counts.items():
        f.write(f"{race}: {count}\n")
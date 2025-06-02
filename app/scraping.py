# Aqui se faz o web scraping para obter as raças e classes permitidas do D&D Beyond
import os
import cloudscraper
import pandas as pd

def get_dnd_data(url):
    scraper = cloudscraper.CloudScraper()
    response = scraper.get(url)
    data = response.json()

    if "raceFluff" in data:
        return list({race["name"] for race in data["raceFluff"]})
    elif "classFluff" in data:
        return [v.get("name", k.replace(".json", "").replace("class-", "")) for k, v in data["classFluff"].items()]
    else:
        return [k.replace(".json", "").replace("class-", "") for k in data.keys()]

# --- Scrape races and classes ---
race_names = get_dnd_data("https://5e.tools/data/fluff-races.json")
class_names = get_dnd_data("https://5e.tools/data/class/index.json")

print("Races:", race_names)
print("Classes:", class_names)

# Caminho para a pasta Data relativo ao ficheiro atual
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data'))
os.makedirs(data_dir, exist_ok=True)

# --- Save races to CSV ---
df_races = pd.DataFrame({'race': sorted(race_names)})
df_races['category'] = 'Unknown'
df_races.to_csv(os.path.join(data_dir, 'unique_races_dict.csv'), index=False)

# --- Save classes to CSV ---
df_classes = pd.DataFrame({'class': sorted(class_names)})
df_classes.to_csv(os.path.join(data_dir, 'unique_classes_list.csv'), index=False)


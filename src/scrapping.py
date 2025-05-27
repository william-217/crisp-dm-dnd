from bs4 import BeautifulSoup
import pandas as pd

with open('races_raw.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

races = []

# Procura todos os <a> de categoria (ex: Common, Exotic, Monstrous)
for li in soup.find_all('li'):
    a = li.find('a', href=True)
    if a and a['href'].startswith('/lineage#toc'):
        category = a.text.strip()
        ul = li.find('ul')
        if ul:
            for race_li in ul.find_all('li'):
                race_a = race_li.find('a', href=True)
                if race_a and race_a['href'].startswith('/lineage:'):
                    race_name = race_a.text.strip()
                    races.append({'race': race_name, 'type': category})

df_races = pd.DataFrame(races)
print(df_races)
# df_races.to_csv('dnd_races.csv', index=False, encoding='utf-8-sig')


#tentativa frustrada||||
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape
url = "https://dnd5e.wikidot.com/lineage"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# STEP 1: Extract ToC entries for valid categories
category_map = {
    "Standard Lineages": "Standard",
    "Exotic Lineages": "Exotic",
    "Monstrous Lineages": "Monstrous",
    "Setting Specific Lineages": "Setting Specific",
    "Custom Lineage": "Custom Lineage"
}

section_anchors = {}
toc_links = soup.select("#toc #toc-list a")
for link in toc_links:
    text = link.text.strip()
    href = link.get("href", "").replace("#", "")
    if text in category_map:
        section_anchors[href] = category_map[text]

# STEP 2: Extract race names from each section's wiki-content-table
races = []
for anchor_id, category in section_anchors.items():
    header = soup.find(id=anchor_id)
    if not header:
        continue
    node = header.find_next_sibling()
    while node:
        if node.name and node.get("id") in section_anchors:
            break  # Stop if next category
        if node.name == "table" and "wiki-content-table" in node.get("class", []):
            for a in node.find_all("a"):
                name = a.text.strip()
                if name:
                    races.append({"original": name, "category": category})
        node = node.find_next_sibling()

# Check if any races were found
if not races:
    raise Exception("No races found. Check structure parsing.")

# STEP 3: Normalize race names
def normalize_race(name):
    name = name.lower()
    if "genasi" in name:
        return "Genasi"
    if "dragonborn" in name:
        return "Dragonborn"
    if "tiefling" in name:
        return "Tiefling"
    if "orc" in name and "half" not in name:
        return "Orc"
    if "half-elf" in name:
        return "Half-Elf"
    if "half-orc" in name:
        return "Half-Orc"
    if "elf" in name:
        return "Elf"
    if "dwarf" in name:
        return "Dwarf"
    if "halfling" in name:
        return "Halfling"
    if "kender" in name:
        return "Kender"
    if "custom" in name:
        return "Custom Lineage"
    return name.title()

# Create DataFrame and normalize
df = pd.DataFrame(races)
df["race"] = df["original"].map(normalize_race)

# Drop duplicate normalized names
df = df.drop_duplicates(subset=["race"]).sort_values(by=["category", "race"]).reset_index(drop=True)

# Reorder columns: race first, then category
df = df[["race", "category"]]

# Output results
print(df)

# Save to CSV
df.to_csv("unique_races_dict.csv", index=False)
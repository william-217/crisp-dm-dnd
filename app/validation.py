import cloudscraper

def get_dnd_data(url):
    scraper = cloudscraper.CloudScraper()
    response = scraper.get(url)
    data = response.json()

    if "raceFluff" in data:
        return list({race["name"] for race in data["raceFluff"]})  # use set for uniqueness, then back to list
    elif "classFluff" in data:
        return [v.get("name", k.replace(".json", "").replace("class-", "")) for k, v in data["classFluff"].items()]
    else:
        # Assume a flat JSON of filenames as in index.json
        return [k.replace(".json", "").replace("class-", "") for k in data.keys()]

# Example usage:
race_names = get_dnd_data("https://5e.tools/data/fluff-races.json")
class_names = get_dnd_data("https://5e.tools/data/class/index.json")

print("Races:", race_names)
print("Classes:", class_names)
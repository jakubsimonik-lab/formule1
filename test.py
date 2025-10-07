print("Ahoj")
import fastf1
import json

fastf1.Cache.enable_cache('cache')
session = fastf1.get_session(2025, 'Qatar', 'R')
session.load()

results = []
for driver in session.results.itertuples():
    results.append({
        "pos": driver.Position,
        "driver": driver.FullName,
        "team": driver.TeamName,
        "points": driver.Points
    })

with open('results.json', 'w') as f:
    json.dump(results, f, indent=2)
session = fastf1.get_session(2025, 'Monza', 'R')
session.load()
print(session.results[["FullName", "TeamName", "Position", "Points"]])
import fastf1
import os
import json
from fastf1 import ergast  # pro rozpis závodů

def fetch_all_race_results_2025():
    # vytvoř cache složku, pokud neexistuje
    os.makedirs('cache', exist_ok=True)
    fastf1.Cache.enable_cache('cache')

    # získání kalendáře závodů
    season = 2025
    schedule = ergast.get_race_schedule(season)  # pomocí ergast submodulu v FastF1

    all_results = []

    for race_info in schedule:
        race_name = race_info["raceName"]
        round_number = race_info["round"]
        circuit = race_info["circuitName"]
        country = race_info["country"]
        date = race_info["date"]

        print(f"Loading race {round_number}: {race_name}")

        try:
            # pokus o načtení dat ze závodu
            session = fastf1.get_session(season, race_name, 'R')
            session.load()

            # přidej všechny výsledky jezdců
            race_results = []
            for driver in session.results.itertuples():
                race_results.append({
                    "position": driver.Position,
                    "driver": driver.FullName,
                    "team": driver.TeamName,
                    "points": driver.Points,
                    "laps": driver.Laps,
                    "race_time": driver.Time,
                    "status": driver.Status  # může být např. DNF, +x.x
                })

            all_results.append({
                "round": round_number,
                "raceName": race_name,
                "circuit": circuit,
                "country": country,
                "date": date,
                "results": race_results
            })

        except Exception as e:
            print(f"Chyba při načítání {race_name}: {e}")
            # zaznamenej i ten závod bez výsledků
            all_results.append({
                "round": round_number,
                "raceName": race_name,
                "circuit": circuit,
                "country": country,
                "date": date,
                "results": None,
                "error": str(e)
            })

    # uloží výstup do JSON
    with open("all_race_results_2025.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print("Hotovo — výsledky uloženy do all_race_results_2025.json")


if __name__ == "__main__":
    print("Začínám stahovat všechny závody 2025…")
    fetch_all_race_results_2025()

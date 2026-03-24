import time
import json
import pandas as pd

# Charger le fichier CSV (même dossier que le script)
df = pd.read_csv("C:/Users/guiry/Pictures/final_final.csv")

# Nettoyage des colonnes (important)
df.columns = df.columns.str.strip()

i = 0

while True:
    row = df.iloc[i]

    data = {
        "server_id": int(row.get("Server ID", 0)),

       
        "cpu_usage": float(row.get("Total CPU Power Consumption (W)", 0)),
        "gpu_usage": float(row.get("Total GPU Power Consumption (W)", 0)),
        "it_power": float(row.get("Total IT Power per Server (W)", 0)),

         
        "energy_ic": float(row.get("Energy Total IC", 0)),
        "energy_ac": float(row.get("Energy Total AC", 0))
    }

    # écrire dans JSON
    with open("data.json", "w") as f:
        json.dump(data, f)

    # boucle infinie
    i += 1
    if i >= len(df):
        i = 0

    time.sleep(1)
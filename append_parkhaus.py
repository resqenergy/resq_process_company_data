import pandas as pd
import os

THIS_PATH = os.path.dirname(os.path.abspath(__file__))

company_area_units_path = os.path.join(
    THIS_PATH,
    "results",
    "companies_area_and_units_per_cluster.csv"
)
geb_grunddatensatz_path = os.path.join(
    THIS_PATH,
    "raw_data",
    "20251128_Gebäudegrunddatensatz_25833.csv"
)

# --------------------------------------------------
# 1. CSV einlesen
# --------------------------------------------------
company_area_units = pd.read_csv(company_area_units_path, sep=",")
geb_grunddatensatz = pd.read_csv(geb_grunddatensatz_path, sep=",")

# --------------------------------------------------
# 2. Parkhäuser filtern
# --------------------------------------------------
mask_parkhaus = geb_grunddatensatz["Geb_teil"].str.contains(
    "Parkhaus",
    case=False,      # Groß-/Kleinschreibung ignorieren
    na=False         # NaN-Werte nicht matchen lassen
)

parkhaus_df = geb_grunddatensatz.loc[mask_parkhaus]

# Fläche aufsummieren
a_parkhaus = parkhaus_df["Geschossflaeche"].sum()

# Anzahl zählen
n_parkhaus = parkhaus_df.shape[0]

# --------------------------------------------------
# 3. Neue Zeile hinzufügen
# --------------------------------------------------
new_row = pd.DataFrame([{
    "Cluster": "Parkhaus",
    "Nutzfläche (m²)": a_parkhaus,
    "Nutzeinheiten": n_parkhaus
}])

company_area_units = pd.concat(
    [company_area_units, new_row],
    ignore_index=True
)

# --------------------------------------------------
# 4. Datei überschreiben
# --------------------------------------------------
company_area_units.to_csv(company_area_units_path, index=False)

import pandas as pd
import os


def swap_columns(filename):
    if os.path.exists(filename):
        # Datei einlesen (dein Format: index;adc)
        df = pd.read_csv(filename, sep=';')

        # Spaltennamen identifizieren (index ist Spalte 0, adc ist Spalte 1)
        cols = df.columns.tolist()

        # Spalten tauschen: Wir wollen [adc, index] für die Library
        df_swapped = df[[cols[1], cols[0]]]

        # Überschreiben der Datei (ohne Index-Spalte von Pandas)
        # Wir nutzen den Tabulator '\t' oder ';' - passend zu deinem späteren Import
        df_swapped.to_csv(filename, sep=';', index=False)
        print(f"Erfolg: {filename} wurde korrigiert.")
    else:
        print(f"Warnung: {filename} nicht gefunden.")


# Liste aller deiner Dateien
files = [
"Weight3.csv"
]

for f in files:
    swap_columns("Labor_3/data_analysis/" + f)

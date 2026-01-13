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
    'MVC1.csv', 'MVC2.csv', 'MVC3.csv',
    'Weight1.csv', 'Weight2.csv', 'Weight3.csv',
    'Fatigue1.csv', 'Fatigue2.csv', 'Fatigue3.csv'
]

for f in files:
    swap_columns("Labor_3/data_analysis/" + f)

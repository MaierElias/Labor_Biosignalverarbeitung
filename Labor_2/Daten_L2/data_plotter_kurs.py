import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Daten einlesen
dateiname = "Labor_2/Daten_L2/Daten_Kurs.csv"
df = pd.read_csv(dateiname, sep=';', decimal=',')

# Daten nach Geschlecht aufteilen
df_women = df[df['Gender'] == 'w']
df_men = df[df['Gender'] == 'm']

# Gruppenname (hier anpassen!)
gruppenname = "Gruppe: Elias, Moritz, Hauke"

# Histogramm 1: Herzfrequenz (HR)
bins1 = np.linspace(df['HR'].min(), df['HR'].max(), 11)
width1 = (bins1[1] - bins1[0]) * 0.4
centers1 = (bins1[:-1] + bins1[1:]) / 2

hist_w1, _ = np.histogram(df_women['HR'], bins=bins1)
hist_m1, _ = np.histogram(df_men['HR'], bins=bins1)

fig1, ax1 = plt.subplots(figsize=(8, 5))
ax1.bar(centers1 - width1/2, hist_w1, width=width1, alpha=0.5, color='pink', 
        label='Frauen', edgecolor='black')
ax1.bar(centers1 + width1/2, hist_m1, width=width1, alpha=0.5, color='lightblue', 
        label='Männer', edgecolor='black')
ax1.set_xlabel('Herzfrequenz [bpm]')
ax1.set_ylabel('Häufigkeit')
# ax1.set_title(f'Verteilung der mittleren Herzfrequenz\n{gruppenname}')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('Labor_2/Daten_L2/graphs/Histogramm_Herzfrequenz.png', dpi=300, bbox_inches='tight')
print("✓ Gespeichert: Labor_2/Daten_L2/graphs/Histogramm_Herzfrequenz.png")
plt.show()
plt.close()

# Histogramm 2: Herzfrequenzvariabilität (HFV)
bins2 = np.linspace(df['HFV'].min(), df['HFV'].max(), 11)
width2 = (bins2[1] - bins2[0]) * 0.4
centers2 = (bins2[:-1] + bins2[1:]) / 2

hist_w2, _ = np.histogram(df_women['HFV'], bins=bins2)
hist_m2, _ = np.histogram(df_men['HFV'], bins=bins2)

fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.bar(centers2 - width2/2, hist_w2, width=width2, alpha=0.5, color='pink', 
        label='Frauen', edgecolor='black')
ax2.bar(centers2 + width2/2, hist_m2, width=width2, alpha=0.5, color='lightblue', 
        label='Männer', edgecolor='black')
ax2.set_xlabel('Herzfrequenzvariabilität [ms]')
ax2.set_ylabel('Häufigkeit')
# ax2.set_title(f'Verteilung der Herzfrequenzvariabilität\n{gruppenname}')
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('Labor_2/Daten_L2/graphs/Histogramm_HFV.png', dpi=300, bbox_inches='tight')
print("✓ Gespeichert: Labor_2/Daten_L2/graphs/Histogramm_HFV.png")
plt.show()
plt.close()

# # Statistische Auswertung
# print("\n=== Statistische Auswertung ===\n")
# print("Herzfrequenz (HR):")
# print(f"  Frauen:  Mittelwert = {df_women['HR'].mean():.2f} bpm, SD = {df_women['HR'].std():.2f}")
# print(f"  Männer:  Mittelwert = {df_men['HR'].mean():.2f} bpm, SD = {df_men['HR'].std():.2f}")
# print(f"\nHerzfrequenzvariabilität (HFV):")
# print(f"  Frauen:  Mittelwert = {df_women['HFV'].mean():.2f} ms, SD = {df_women['HFV'].std():.2f}")
# print(f"  Männer:  Mittelwert = {df_men['HFV'].mean():.2f} ms, SD = {df_men['HFV'].std():.2f}")
# print(f"\nAnzahl Messungen: Frauen = {len(df_women)}, Männer = {len(df_men)}")
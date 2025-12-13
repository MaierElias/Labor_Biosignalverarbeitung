import pandas as pd
import plotly.graph_objects as go
import numpy as np

import Lab2Functions as ekg

import matplotlib as mpl
import matplotlib.pyplot as plt

data = {
    "Elias": pd.read_csv('Labor_2/Daten_L2/arduino_log_Elias.csv', sep=";", index_col=0),
    "Lasse": pd.read_csv('Labor_2/Daten_L2/arduino_log_Lasse.csv', sep=";", index_col=0),
    "Hauke": pd.read_csv('Labor_2/Daten_L2/arduino_log_Hauke.csv', sep=";", index_col=0),
    "with_charger": pd.read_csv('Labor_2/Daten_L2/data_with_charger.csv', sep=";", index_col=0),
    "without_charger":  pd.read_csv('Labor_2/Daten_L2/data_without_charger.csv', sep=";", index_col=0),
    "with_charger_and_touch": pd.read_csv('Labor_2/Daten_L2/data_with_charger_and_touch.csv', sep=";", index_col=0)
}

names = [name for name in data]

for name, df in data.items():
    max_threshold = 1000
    filter_mask = df['value'] <= max_threshold
    data[name] = df[filter_mask]


def create_plot(name):
    ecg_signal = data[name]["value"][5000:10000].to_list()
    time = data[name].index[:5000].to_list()

    # 3. Plot erstellen, Segmente farbig zeichnen und Text hinzufügen
    plt.figure(figsize=(10, 5))

    # Basislinie und Segmente (wie im vorherigen Beispiel)
    P_start, P_end = 0, 235
    p_pos_index = int((P_start+P_end)/2)
    QRS_start, QRS_end = 235, 350
    qrs_r_pos_index = int((QRS_start+QRS_end)/2)
    T_start, T_end = 350, 660
    t_pos_index = int((T_start+T_end)/2)
    Baseline_color = '#CCCCCC'

    plt.plot(time, ecg_signal, color=Baseline_color, linewidth=2)
    plt.plot(time[P_start:P_end], ecg_signal[P_start:P_end],
             color='red', linewidth=3)
    plt.plot(time[QRS_start:QRS_end],
             ecg_signal[QRS_start:QRS_end], color='green', linewidth=3)
    plt.plot(time[T_start:T_end], ecg_signal[T_start:T_end],
             color='orange', linewidth=3)

    # 4. Textbeschriftung direkt am Graphen (oberhalb der Peaks)
    text_offset_y = 2  # Kleiner vertikaler Abstand über dem Peak

    # P-Welle

    y_P = max(ecg_signal[P_start:P_end]) + text_offset_y
    plt.text(time[p_pos_index], y_P, 'P', color='red',
             fontsize=14, fontweight='bold', ha='center')

    # QRS-Komplex (R-Peak)
    y_QRS = max(ecg_signal[QRS_start:QRS_end]) + text_offset_y
    plt.text(time[qrs_r_pos_index], y_QRS, 'QRS', color='green',
             fontsize=14, fontweight='bold', ha='center')

    # T-Welle
    y_T = max(ecg_signal[T_start:T_end]) + text_offset_y
    plt.text(time[t_pos_index], y_T, 'T', color='orange',
             fontsize=14, fontweight='bold', ha='center')

    # Achsenbeschriftungen und Titel
    plt.xlabel('Zeit (ms)')
    plt.ylabel('Amplitude')
    plt.grid(True, which='both', linestyle=':', linewidth=0.5)
    plt.ylim(min(ecg_signal) - 0.2, max(ecg_signal) + 0.3)  # Y-Achse angepasst
    plt.show()

def create_plots():
    for name in ["Elias", "Lasse", "Hauke"]:
        create_plot(name)


def analyse(name):
    """Analysiere ECG-Daten und berechne HF und HRV"""

    ecg = data[name]["value"]
    time = pd.Series(np.arange(len(ecg)))

    d_ECG, peaks_d_ecg = ekg.decg_peaks(ecg, time)
    Rwave_peaks_d_ecg, threshold = ekg.d_ecg_peaks(
        d_ECG, peaks_d_ecg, time, 1, 0.2)
    Rwave_t = ekg.Rwave_peaks(ecg, d_ECG, Rwave_peaks_d_ecg, time)

    sampling_rate = 1000  # Hz
    RR_intervals = np.diff(Rwave_t)
    RR_intervals_seconds = RR_intervals / sampling_rate
    mean_RR_interval = np.mean(RR_intervals_seconds)
    heart_rate_bpm = 60 / mean_RR_interval
    hrv = (np.std(RR_intervals_seconds))*1000  # in ms

    return heart_rate_bpm, hrv, Rwave_t


# Berechnung des geschätzten Energieverbrauchs für jede Person
person_data = {
    "Elias": {"age": 21, "weight": 73},
    "Lasse": {"age": 19, "weight": 58},
    "Hauke": {"age": 21, "weight": 77}
}

results = {}
for name in ["Elias", "Lasse", "Hauke"]:
    heart_rate, hrv, Rwave_t = analyse(name)
    age = person_data[name]["age"]
    weight = person_data[name]["weight"]
    # Energieverbrauch in kcal/min (vereinfachte Formel)
    #hrr = heart_rate - (208 - 0.7 * age)
    #energy_expenditure = 0.449+0.0627*hrr+0.00743*weight+0.001*hrr*weight # in kcal/minute Model one from given paper for man and low activity
    energy_expenditure = 4.56 - 0.0265*heart_rate -0.1506*weight + 0.00189*heart_rate*weight  # in kcal/minute Model one from given paper and low activity
    
    results[name] = {
        "Heart Rate (bpm)": float(heart_rate),
        "HRV (ms)": float(hrv),
        "Estimated Energy Expenditure (kcal/min)": float(energy_expenditure),
        "Estimated Energy Expenditure * duration (kcal)": float(energy_expenditure * 10)  # assuming 10 minutes of activity
    }
    print(results[name])
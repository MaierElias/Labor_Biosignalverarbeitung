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
    QRS_starts = [230]
    QRS_ends = [350]
    T_starts = [350]
    T_ends = [660]
    P_start = [0]
    P_end = [235]

    for i in range(len(QRS_starts)):
        color_graph(time, ecg_signal, QRS_starts[i], QRS_ends[i],
                    T_starts[i], T_ends[i], P_start, P_end)

    # Achsenbeschriftungen und Titel
    plt.xlabel('Zeit (ms)')
    plt.ylabel('Amplitude')
    plt.grid(True, which='both', linestyle=':', linewidth=0.5)
    plt.ylim(min(ecg_signal) - 0.2, max(ecg_signal) + 0.3)  # Y-Achse angepasst
    plt.show()


def color_graph(time, ecg_signal, QRS_start, QRS_end, T_start, T_end, P_start, P_end):
    Baseline_color = '#CCCCCC'
    p_pos_index = int((P_start+P_end)/2)
    qrs_r_pos_index = int((QRS_start+QRS_end)/2)
    t_pos_index = int((T_start+T_end)/2)

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


for name in ["Elias", "Lasse", "Hauke"]:
    create_plot(name)

create_plots()

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


def plot_ecg_with_rwaves(name, Rwave_t):
    ecg_signal = data[name]["value"].to_list()
    time = data[name].index.to_list()

    # Zeitraum definieren
    start_idx = 6000
    end_idx = 11000
    
    # Daten für den gewünschten Zeitraum extrahieren
    time_range = time[start_idx:end_idx]
    ecg_range = ecg_signal[start_idx:end_idx]
    
    # R-Peaks im Zeitraum filtern
    mask = (Rwave_t >= start_idx) & (Rwave_t < end_idx)
    rwave_indices = Rwave_t[mask]
    
    plt.figure(figsize=(10, 5))
    plt.plot(time_range, ecg_range, color='#1f77b4', linewidth=1, label='ECG Signal')
    plt.scatter([time[i] for i in rwave_indices], [ecg_signal[i] for i in rwave_indices],
                color='red', label='R-Peaks', zorder=5)
    plt.xlabel('Zeit / $ms$')
    plt.ylabel('Amplitude')
    plt.grid(True, which='both', linestyle=':', linewidth=0.5)
    plt.legend(loc = 'upper right')
    plt.savefig(f'Bericht2_Biosignalverarbeitung/figures/ecg_with_rwaves_{name}.png', dpi=300, bbox_inches='tight')
    plt.show()

plot_ecg_with_rwaves("Elias", analyse("Elias")[2])

# Berechnung des geschätzten Energieverbrauchs für jede Person
def calculate_energy_expenditure():
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

calculate_energy_expenditure()

def create_serial_plotter_plots():
    fig, axes = plt.subplots(2, 1, figsize=(10, 10)) # 2 Zeilen, 1 Spalte
    
    for idx, name in enumerate(["with_charger", "with_charger_and_touch"]):
        ecg_signal = data[name]["value"].to_list()
        time = data[name].index.to_list()

        axes[idx].plot(time, ecg_signal, color='#1f77b4', linewidth=1)
        axes[idx].set_xlabel('Zeit / $ms$', fontsize=10)
        axes[idx].set_ylabel('Amplitude', fontsize=10)
        #axes[idx].set_title(f'ECG Signal - {name.replace("_", " ").title()}', fontsize=12, fontweight='bold', pad=15)
        axes[idx].grid(True, which='both', linestyle=':', linewidth=0.5)
        #axes[idx].set_ylim(min(ecg_signal) - 0.2, max(ecg_signal) + 0.3)
        axes[idx].tick_params(axis='both', which='major', labelsize=9)
    
    plt.tight_layout(pad=2.0)
    plt.savefig('Labor_2/Daten_L2/graphs/ecg_plots_with_and_without_charger.png', dpi=300, bbox_inches='tight')
    plt.show()

create_serial_plotter_plots()

def plot_of_all_participants():
    plt.figure(figsize=(12, 6))

    for name in ["Elias", "Lasse", "Hauke"]:
        ecg_signal = data[name]["value"][6000:11000].to_list()
        time = data[name].index[6000:11000].to_list()

        plt.plot(time, ecg_signal, label=name)

    plt.xlabel('Zeit / $ms$')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True, which='both', linestyle=':', linewidth=0.5)
    plt.savefig('Bericht2_Biosignalverarbeitung/figures/ecg_plots_all_participants.png', dpi=300, bbox_inches='tight')
    plt.show()

plot_of_all_participants()
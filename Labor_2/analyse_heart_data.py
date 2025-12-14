import pandas as pd
import scipy.signal as sps
import numpy as np
import Lab2Functions as ekg
import matplotlib.pyplot as plt


def analyze_ecg(file_path, name="Default_name"):
    """Analysiere ECG-Daten und berechne HF und HRV"""
    ecg = pd.read_csv(file_path, sep=';')
    ecg = ecg['value']
    time = pd.Series(np.arange(len(ecg)))

    d_ECG, peaks_d_ecg = ekg.decg_peaks(ecg, time)
    Rwave_peaks_d_ecg, threshold = ekg.d_ecg_peaks(
        d_ECG, peaks_d_ecg, time, 0.9, 0.2)
    Rwave_t = ekg.Rwave_peaks(ecg, d_ECG, Rwave_peaks_d_ecg, time)

    sampling_rate = 1000  # Hz
    RR_intervals = np.diff(Rwave_t)
    RR_intervals_seconds = RR_intervals / sampling_rate
    mean_RR_interval = np.mean(RR_intervals_seconds)
    heart_rate_bpm = 60 / mean_RR_interval
    hrv = (np.std(RR_intervals_seconds))*1000  # in ms

    print(f'\n{name}:')
    print(f'Heart Rate: {heart_rate_bpm:.2f} bpm')
    print(f'Heart Rate Variability (HRV): {hrv:.4f} milliseconds')

    return heart_rate_bpm, hrv

# files = {
#     'Hauke': 'Labor_2/Daten_L2/arduino_log_Hauke.csv',
#     'Elias': 'Labor_2/Daten_L2/arduino_log_Elias.csv',
#     'Lasse': 'Labor_2/Daten_L2/arduino_log_Lasse.csv'
# }

# results = {}
# for name, file_path in files.items():
#     results[name] = analyze_ecg(file_path, name)

# -------------------------------------------


def analyze_ecg_and_plot(file_path, window_size=10):
    """Analysiere ECG-Daten und erstelle Plot der Herzfrequenz mit gleitendem Fenster

    Parameters:
    -----------
    file_path : str
        Pfad zur ECG-Datei
    window_size : int
        Anzahl der R-R-Intervalle für die Fensterberechnung (default: 10)
    """

    # Daten laden - als Pandas Series für Kompatibilität
    df = pd.read_csv(file_path, sep=';')
    ecg = df['value']  # Als Pandas Series behalten!
    time = pd.Series(df['index'].values)  # Als Series

    print(f"Geladene Datenpunkte: {len(ecg)}")
    print(f"Zeitbereich: {time.iloc[0]} - {time.iloc[-1]} ms")
    print(f"Signal-Bereich: {ecg.min():.2f} - {ecg.max():.2f} mV")

    # ECG-Analyse mit angepassten Parametern
    d_ECG, peaks_d_ecg = ekg.decg_peaks(ecg, time)

    print(f"Gefundene d_ECG Peaks: {len(peaks_d_ecg)}")

    # Versuche Peak-Detection mit verschiedenen Parametern
    try:
        # Erste Versuche mit moderaten Werten
        Rwave_peaks_d_ecg, threshold = ekg.d_ecg_peaks(
            d_ECG, peaks_d_ecg, time, 0.01, 0.1)
        print(
            f"Versuch 1 erfolgreich: {len(Rwave_peaks_d_ecg)} R-Wave Peaks gefunden")
    except Exception as e:
        print(f"Versuch 1 fehlgeschlagen: {e}")
        try:
            # Zweiter Versuch mit niedrigeren Schwellen
            Rwave_peaks_d_ecg, threshold = ekg.d_ecg_peaks(
                d_ECG, peaks_d_ecg, time, 0.3, 0.15)
            print(
                f"Versuch 2 erfolgreich: {len(Rwave_peaks_d_ecg)} R-Wave Peaks gefunden")
        except Exception as e2:
            print(f"Versuch 2 fehlgeschlagen: {e2}")
            try:
                # Dritter Versuch mit sehr niedrigen Schwellen
                Rwave_peaks_d_ecg, threshold = ekg.d_ecg_peaks(
                    d_ECG, peaks_d_ecg, time, 0.2, 0.1)
                print(
                    f"Versuch 3 erfolgreich: {len(Rwave_peaks_d_ecg)} R-Wave Peaks gefunden")
            except Exception as e3:
                print(f"Versuch 3 fehlgeschlagen: {e3}")
                print("\n❌ Alle Peak-Detection Versuche fehlgeschlagen!")
                print("Das Signal ist vermutlich zu verrauscht oder beschädigt.")
                return None, None

    # R-Wave Peaks extrahieren
    try:
        Rwave_t = ekg.Rwave_peaks(ecg, d_ECG, Rwave_peaks_d_ecg, time)
    except Exception as e:
        print(f"❌ Fehler bei Rwave_peaks: {e}")
        return None, None

    sampling_rate = 1000  # Hz

    # Rwave_t in numpy array konvertieren für einfachere Handhabung
    Rwave_t_values = Rwave_t.values

    RR_intervals = np.diff(Rwave_t_values)
    RR_intervals_seconds = RR_intervals / sampling_rate

    # Filtern von unrealistischen RR-Intervallen (< 0.3s oder > 2s)
    valid_mask = (RR_intervals_seconds > 0.3) & (RR_intervals_seconds < 2.0)
    RR_intervals_seconds = RR_intervals_seconds[valid_mask]

    print(f"\nAnzahl R-Peaks: {len(Rwave_t)}")
    print(
        f"Anzahl RR-Intervalle (nach Filterung): {len(RR_intervals_seconds)}")

    if len(RR_intervals_seconds) < 3:
        print("\n⚠️ WARNUNG: Zu wenige valide RR-Intervalle!")
        return None, None

    # Prüfen ob genug Daten vorhanden sind
    if len(RR_intervals_seconds) < window_size:
        print(f"\nWARNUNG: Nur {len(RR_intervals_seconds)} RR-Intervalle!")
        window_size = max(1, len(RR_intervals_seconds))

    # Herzfrequenz mit gleitendem Fenster berechnen
    windowed_hr = []
    windowed_times = []

    # Angepasste Zeitpunkte für gefilterte Daten - ALS NUMPY ARRAY!
    valid_peak_times = Rwave_t_values[:-1][valid_mask]

    for i in range(len(RR_intervals_seconds) - window_size + 1):
        window = RR_intervals_seconds[i:i+window_size]
        mean_RR = np.mean(window)
        hr = 60 / mean_RR
        windowed_hr.append(hr)
        # Jetzt funktioniert der Zugriff, weil valid_peak_times ein numpy array ist
        windowed_times.append(valid_peak_times[i + window_size//2])

    windowed_hr = np.array(windowed_hr)
    windowed_times = np.array(windowed_times)

    # Gesamtdurchschnittswerte
    mean_RR_interval = np.mean(RR_intervals_seconds)
    heart_rate_bpm = 60 / mean_RR_interval
    hrv = (np.std(RR_intervals_seconds)) * 1000  # in ms

    print(f"\n✅ Ergebnisse:")
    print(f"Anzahl Fenster-Werte: {len(windowed_hr)}")
    print(f"Mittlere HR: {heart_rate_bpm:.2f} bpm")
    print(f"HRV: {hrv:.2f} ms")

    if len(windowed_hr) > 0:
        print(
            f"Zeit-Bereich: {windowed_times.min():.2f} - {windowed_times.max():.2f} ms")
        print(
            f"HR-Bereich: {windowed_hr.min():.2f} - {windowed_hr.max():.2f} bpm")

        # Plot erstellen

        plt.figure(figsize=(12, 6))
        [120, 120+180, 120+180+300]

        plt.plot(windowed_times, windowed_hr, marker='o', linestyle='-',
                 linewidth=2, markersize=4, color='#1f77b4')

        plt.axvline(120*1000)
        plt.axvline((120+180)*1000)
        plt.axvline((120+180+300)*1000)

        plt.xlabel('Zeit / $ms$', fontsize=12)
        plt.ylabel('Herzfrequenz / $bpm$', fontsize=12)
        plt.title(f'Herzfrequenz während Belastung (Fenster={window_size} Schläge)',
                  fontsize=14, fontweight='bold')
        plt.grid(True, which='both', linestyle=':', linewidth=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig('Bericht2_Biosignalverarbeitung/figures/windowed_hr.png',
                    dpi=300, bbox_inches='tight')
        plt.show()
    else:
        print("\n❌ Keine Daten zum Plotten!")

    return heart_rate_bpm, hrv


# Verwendung:
analyze_ecg_and_plot(
    'Labor_2/Daten_L2/arduino_log_belastung.csv', window_size=7)

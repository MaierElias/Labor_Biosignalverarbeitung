import pandas as pd
import scipy.signal as sps
import numpy as np
import Lab2Functions as ekg
import plotly.graph_objects as go


def analyze_ecg(file_path, name):
    """Analysiere ECG-Daten und berechne HF und HRV"""
    ecg = pd.read_csv(file_path, sep=';')
    ecg = ecg['value']
    time = pd.Series(np.arange(len(ecg)))
    
    d_ECG, peaks_d_ecg = ekg.decg_peaks(ecg, time)
    Rwave_peaks_d_ecg, threshold = ekg.d_ecg_peaks(d_ECG, peaks_d_ecg, time, 1, 0.2)
    Rwave_t = ekg.Rwave_peaks(ecg, d_ECG, Rwave_peaks_d_ecg, time)
    
    sampling_rate = 1000  # Hz
    RR_intervals = np.diff(Rwave_t)
    RR_intervals_seconds = RR_intervals / sampling_rate
    mean_RR_interval = np.mean(RR_intervals_seconds)
    heart_rate_bpm = 60 / mean_RR_interval
    hrv = (np.std(RR_intervals_seconds))*1000 # in ms
    
    print(f'\n{name}:')
    print(f'Heart Rate: {heart_rate_bpm:.2f} bpm')
    print(f'Heart Rate Variability (HRV): {hrv:.4f} milliseconds')
    
    return heart_rate_bpm, hrv

files = {
    'Hauke': 'Labor_2/Daten_L2/arduino_log_Hauke.csv',
    'Elias': 'Labor_2/Daten_L2/arduino_log_Elias.csv',
    'Lasse': 'Labor_2/Daten_L2/arduino_log_Lasse.csv'
}

results = {}
for name, file_path in files.items():
    results[name] = analyze_ecg(file_path, name)
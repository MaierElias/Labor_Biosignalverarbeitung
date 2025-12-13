import pandas as pd
import plotly.graph_objects as go

data = {
    "Elias": pd.read_csv('Labor_2/Daten_L2/arduino_log_Elias.csv', sep=";", index_col=0),
    "Lasse": pd.read_csv('Labor_2/Daten_L2/arduino_log_Lasse.csv', sep=";", index_col=0),
    "Hauke": pd.read_csv('Labor_2/Daten_L2/arduino_log_Hauke.csv', sep=";", index_col=0),
    "with_charger": pd.read_csv('Labor_2/Daten_L2/data_with_charger.csv', sep=";", index_col=0),
    "without_charger":  pd.read_csv('Labor_2/Daten_L2/data_without_charger.csv', sep=";", index_col=0),
    "with_charger_and_touch": pd.read_csv('Labor_2/Daten_L2/data_with_charger_and_touch.csv', sep=";", index_col=0)
}

for name, df in data.items():
    max_threshold = 1000
    filter_mask = df['value'] <= max_threshold
    data[name] = df[filter_mask]


def create_plot(name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data[name].index, y=data[name]["value"],
                             mode='lines', name='Data Series 1'))
    fig.write_image(f"Labor_2/Daten_L2/graphs/{name}_graph.png", format="png")


names = [name for name in data]

for name in names:
    create_plot(name)

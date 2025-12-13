import pandas as pd

df_withoutChrager = pd.read_csv(
    'Labor_2/Daten_L2/Daten_ohneNetzteil.csv', sep=",")

df_withChrager = pd.read_csv(
    'Labor_2/Daten_L2/Daten_mitNetzteil.csv', sep=",")


def swap_columns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df


df_withChrager = swap_columns(df_withChrager, 'value', 'index')
df_withoutChrager = swap_columns(df_withoutChrager, 'value', 'index')


df_withChrager.to_csv("Labor_2/Daten_L2/data_with_charger.csv", sep=";",
                      index=False, header=["index", "value"])


df_withoutChrager.to_csv("Labor_2/Daten_L2/data_without_charger.csv", sep=";",
                         index=False, header=["index", "value"])

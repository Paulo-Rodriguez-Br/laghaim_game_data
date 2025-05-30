import re
from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd
import xlwings as xw

from support_functions_analysis import expand_levels
from sqlit3_queries import (
    query_daily_mean,
    query_interval_mean,
    query_amount_players_per_date,
)

input_path = r"C:\Users\paulo\Desktop\Projet_laghaim\input"

# Extract the level intervals of leveling maps
df_maps = pd.read_excel(r"C:\Users\paulo\Desktop\Projet_laghaim\mapas.xlsx")

# Extract data from log and clean it to put in a dataframe
pattern = re.compile(r'^(.*?),.*?CI:([^:]+):CL:([^:]+)')

files = [file for file in Path(input_path).iterdir() if file.is_file()]
dfs = []

for file in files:
    extracted_lines = []
    with open(str(file), 'r') as file_opened:
        for line in file_opened:
            match = pattern.search(line)
            if match:
                date_time = match.group(1).strip()
                ci = match.group(2)
                cl = match.group(3)
                extracted_lines.append({
                    'date': date_time,
                    'CI': ci,
                    'CL': cl
                })
    dfs.append(pd.DataFrame(extracted_lines))

df = pd.concat(dfs, ignore_index=True)

df['CL'] = df['CL'].astype(int)
df = df.loc[(df['CI'] != 0) & (df['CL'] != 0)].dropna().sort_values(by='date')
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')

# Transform the date in intervals of two hours
hours = df['date'].dt.hour + df['date'].dt.minute / 60
bins = np.arange(0, 25, 2)
labels = [f'{str(h).zfill(2)}:00–{str(h+2).zfill(2)}:00' for h in bins[:-1]]
df['TimeInterval'] = pd.cut(hours, bins=bins, labels=labels, right=False)

# Once you have the interval time, you can get just the date information
df['date'] = pd.to_datetime(df['date']).dt.strftime('%d/%m/%Y')

# Apply the maps dataframe to know where the player was leveling
intervals = pd.IntervalIndex.from_arrays(df_maps['lvl_min_map'], df_maps['lvl_max_map'], closed='both')
df['interval_index'] = intervals.get_indexer(df['CL'])
df['Map'] = df['interval_index'].apply(lambda i: df_maps.iloc[i]['Map'] if i != -1 else None)
df['lvl_min_map'] = df['interval_index'].apply(lambda i: df_maps.iloc[i]['lvl_min_map'] if i != -1 else None)
df['lvl_max_map'] = df['interval_index'].apply(lambda i: df_maps.iloc[i]['lvl_max_map'] if i != -1 else None)
df.drop(columns=['interval_index'], inplace=True)

# Expand the levels
df = expand_levels(df, df_maps)

# Obtain dataframes through SQL queries
conn = sqlite3.connect(":memory:")
df.to_sql("table_master", conn, index=False, if_exists="replace")
df_daily_mean = pd.read_sql_query(query_daily_mean, conn)
df_interval_mean = pd.read_sql_query(query_interval_mean, conn)
df_amount_players_per_date = pd.read_sql_query(query_amount_players_per_date, conn)

# Update Excel without deleting slicers or tables
excel_path = r"C:\Users\paulo\Desktop\Projet_laghaim\relatorio_up.xlsx"
app = xw.App(visible=False)
wb = xw.Book(excel_path)

wb.sheets['Dados_Daily_Mean'].range('A1').options(index=False).value = df_daily_mean
wb.sheets['Dados_Interval_Mean'].range('A1').options(index=False).value = df_interval_mean
wb.sheets['Dados_Amount_Players'].range('A1').options(index=False).value = df_amount_players_per_date

wb.save()
wb.close()
app.quit()

print("Updated Date")






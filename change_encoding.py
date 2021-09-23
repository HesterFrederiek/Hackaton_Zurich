import pandas as pd
import requests
import os
import credentials

# https://github.com/statistikZH/statbot/edit/main/hackathon_hackzurich/input_data/EN_T_SPATIALUNIT.csv


url = 'https://raw.githubusercontent.com/statistikZH/statbot/main/hackathon_hackzurich/input_data/EN_T_SPATIALUNIT.csv'
req = requests.get(url, proxies=credentials.proxies)
with open(os.path.join(credentials.path_spat, credentials.file_name_spat), 'wb') as f:
    f.write(req.content)
print(f'Reading current csv into data frame...')

df_Spatial = pd.read_csv(credentials.file_name_spat, encoding="cp1252",
                         dtype={'BFS_NR': 'Int64', 'DISTRICT_ID': 'Int64', 'REGION_ID': 'Int64',
                                'COMMUNE_TYPE_ID': 'Int64', 'ZIP': 'Int64', 'HEIGHT': 'Int64'})

for i in range(202):
    df_Spatial.iloc[i, 2] = df_Spatial.iloc[i, 2].replace('ü', 'ue')
    df_Spatial.iloc[i, 2] = df_Spatial.iloc[i, 2].replace('ä', 'ae')
    df_Spatial.iloc[i, 2] = df_Spatial.iloc[i, 2].replace('ö', 'oe')
    df_Spatial.iloc[i, 4] = df_Spatial.iloc[i, 4].replace('ü', 'ue')
    df_Spatial.iloc[i, 4] = df_Spatial.iloc[i, 4].replace('ä', 'ae')
    df_Spatial.iloc[i, 4] = df_Spatial.iloc[i, 4].replace('ö', 'oe')

print(df_Spatial["NAME"])

print(df_Spatial['NAME'][200])
print(df_Spatial['NAME_COMBINED'][200])

print(df_Spatial.iloc[3, 2])

df_Spatial.to_csv("EN_T_SPATIALUNIT.csv", index=False)

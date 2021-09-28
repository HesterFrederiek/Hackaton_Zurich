"""
add indicators 998 and 999 for Wohnviertel, the data has been assembled in the geodaten.ipynb file
"""
import pandas as pd
import os
import credentials
import numpy as np


df1 = pd.read_csv("ladestationen_wohnviertel.csv", index_col=None)
df2 = pd.read_csv("ladestationen_wohnviertel_per_1000.csv", index_col=None)

""""
export_file_name = os.path.join(credentials.local_path, credentials.local_file_name)
df1.to_csv(export_file_name, mode='a', header=False, index=False)
df2.to_csv(export_file_name, mode='a', header=False, index=False)
"""

"""
Add Wohnviertel to EN_T_SPATIALUNIT.csv
"""

df3 = pd.read_csv("ladestationen_with_name.csv")

df = pd.DataFrame(columns=["SPATIALUNIT_ID", "TYPE_ID", "NAME", "BFS_NR", "NAME_COMBINED", "DISTRICT_ID", "REGION_ID",
                 "COMMUNE_TYPE_ID", "ZIP", "TEL", "FAX", "HOMEPAGE", "EMAIL", "ADRESSE", "HEIGHT", "AREA"])

df["SPATIALUNIT_ID"] = df3["SPATIAL_UNIT"]
df["TYPE_ID"] = 10
df["NAME"] = df3["WOV_NAME"]
df["NAME_COMBINED"] = df3["WOV_NAME"]
df = df.replace(np.nan, '', regex=True)

print(df)

export_file_name = os.path.join(credentials.local_path, credentials.local_file_name_spatial)
df.to_csv(export_file_name, mode='a', header=False, index=False)


import pandas as pd
import numpy as np



skiprows = [x for x in range(40) if x!=31]
print(skiprows)

usecols=[x for x in range(3,30) if x!=8]

df = pd.read_excel("Motorfahrzeugbestand.xlsx", sheet_name="Zeitreihe", skiprows=skiprows, usecols=usecols)

print(df.columns)
data = list(df.columns)
print(data)

years = []
import pandas as pd
import numpy as np
from datetime import date


# read in available data
df_Motorfahrzeugbestand = pd.read_excel("t11-1-01.xlsx")
df_Bestand_Strassenfahrzeuge = pd.read_excel("t11-1-02.xlsx")
df_Neue_Inverkehrsetzungen = pd.read_excel("t11-1-03.xlsx")



"""
399,Passenger cars per 1000 inhabitants [no.] ,
"Passenger cars registered on September 30, divided by the population in thousands. 
The value is also called motorization rate. 
Note: The value for the entire canton includes all cars with a Zurich license plate; these may also belong to persons or companies not domiciled in the canton of Zurich.",,,,,,
"""

#extract rows with data and year
skiprows_data = [x for x in range(40) if x!=31]
skiprows_year = [x for x in range(40) is x!=8]
usecols=[x for x in range(3,30) if x!=8]


data_row = list(pd.read_excel("t11-1-01.xlsx", sheet_name="Zeitreihe", skiprows=skiprows_data, usecols=usecols).columns)
year_row = list(pd.read_excel("t11-1-01.xlsx", sheet_name="Zeitreihe", skiprows=skiprows_data, usecols=usecols).columns)

print(data_row)
print(year_row)

# make dataframe with our data
df_BS_PassengerCars = pd.dataframe()
INDICATOR_ID = 399
SPATIALUNIT_ID = 1001
VALUE_ADDITION = ""
CAT = date.today()

print(CAT)


# merge with "EN_INDICATORS_VALUES.csv"


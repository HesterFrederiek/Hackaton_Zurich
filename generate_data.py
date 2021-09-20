import pandas as pd
import numpy as np
import datetime
import requests
import os
import credentials

# read in available data, source: https://www.statistik.bs.ch/zahlen/tabellen/11-verkehr-mobilitaet/motorfahrzeuge.html
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
skiprows_year = [x for x in range(40) if x!=7]
usecols=[x for x in range(3,30) if x!=8]


data_row = list(pd.read_excel("t11-1-01.xlsx", sheet_name="Zeitreihe", skiprows=skiprows_data, usecols=usecols).columns)
year_row = list(pd.read_excel("t11-1-01.xlsx", sheet_name="Zeitreihe", skiprows=skiprows_year, usecols=usecols).columns)

#print(data_row)
#print(year_row)

# make dataframe with our data
df_BS_PassengerCars = pd.DataFrame(columns=["INDICATOR_ID", "SPATIALUNIT_ID", "YEAR", "VALUE", "VALUE_ADDITION", "CAT"])
INDICATOR_ID = 399
SPATIALUNIT_ID = 1001
VALUE_ADDITION = np.nan
CAT = str(datetime.datetime.today().strftime('%d.%m.%y %H:%M'))

df_BS_PassengerCars["YEAR"] = year_row
df_BS_PassengerCars["VALUE"] = data_row
df_BS_PassengerCars["INDICATOR_ID"] = INDICATOR_ID
df_BS_PassengerCars["SPATIALUNIT_ID"] = SPATIALUNIT_ID
df_BS_PassengerCars["VALUE_ADDITION"] = VALUE_ADDITION
df_BS_PassengerCars["CAT"] = CAT


# add data to "EN_INDICATORS_VALUES.csv"
export_file_name = os.path.join(credentials.local_path, credentials.local_file_name)
df_BS_PassengerCars.to_csv(export_file_name, mode='a', header=False, index=False)


"""
601,PW new registrations per 1000 inhabitants [amount],
"Passenger cars put on the road for the first time between October 1 of the previous year and September 30, 
divided by the population in thousands. 
Note: The value for the entire canton includes all cars with a Zurich license plate; 
these may also belong to persons or companies not domiciled in the canton of Zurich.",,,,,,
"""

# get our data

years = [x for x in range(2013, 2021)]
skiprows_data = [x for x in range(40) if x!=9]
usecols_1 = [x for x in range(12, 15)]
usecols_2 = [x for x in range(3, 12)]

cars =[]
for year in years:
    data_row_1 = list(pd.read_excel("t11-1-03.xlsx", sheet_name=str(year-1), skiprows=skiprows_data, usecols=usecols_1).columns)
    data_row_2 = list(pd.read_excel("t11-1-03.xlsx", sheet_name=str(year), skiprows=skiprows_data, usecols=usecols_2).columns)
    data_row_1 = [int(float(x)) for x in data_row_1]
    data_row_2 = [int(float(x)) for x in data_row_2]
    #print(data_row_1)
    #print(data_row_2)
    total = np.sum(data_row_1) + np.sum(data_row_2)
    cars.append(total)

print(cars)


#population in thousands, taking from the Motorfahrzeugbestand file
#Die mittlere Wohnbevölkerung entspricht dem Mittelwert der zwölf Monatsmittel; seit 2019 ohne Grenzgänger mit Wochenaufenthalt.
population = 194840/1000

# make dataframe with our data
df_BS_NewRegistrations = pd.DataFrame(columns=["INDICATOR_ID", "SPATIALUNIT_ID", "YEAR", "VALUE", "VALUE_ADDITION", "CAT"])
df_BS_NewRegistrations['YEAR'] = years
df_BS_NewRegistrations['VALUE'] = np.array(cars)/population
df_BS_NewRegistrations['INDICATOR_ID'] = 601
df_BS_NewRegistrations['SPATIALUNIT_ID'] = SPATIALUNIT_ID
df_BS_NewRegistrations['VALUE_ADDITION'] = VALUE_ADDITION
df_BS_NewRegistrations['CAT'] = CAT

# add data to "EN_INDICATORS_VALUES.csv"
export_file_name = os.path.join(credentials.local_path, credentials.local_file_name)
df_BS_NewRegistrations.to_csv(export_file_name, mode='a', header=False, index=False)

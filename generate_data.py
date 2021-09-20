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
"""
export_file_name = os.path.join(credentials.local_path, credentials.local_file_name)
df_BS_PassengerCars.to_csv(export_file_name, mode='a', header=False, index=False)
"""


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

""""
# add data to "EN_INDICATORS_VALUES.csv"
export_file_name = os.path.join(credentials.local_path, credentials.local_file_name)
df_BS_NewRegistrations.to_csv(export_file_name, mode='a', header=False, index=False)
"""

"""
997,Total of electric and hybrid motor cars stock [%],
Share of passenger cars (PW) with either electric or hybrid drive in all passenger cars registered as of September 30; 
hybrid drive refers to all combinations of electric motor and combustion engine
"""


# get number of total cars
skiprows_data = [x for x in range(40) if x!=11]
usecols=[28, 29]
allcars = np.array(pd.read_excel("t11-1-01.xlsx", sheet_name="Zeitreihe", skiprows=skiprows_data, usecols=usecols).columns)
#print(allcars)

# get number of electric + hybrid cars
skiprows_data = [x for x in range(40) if x!=12]
usecols=[28, 29]
electric_cars = np.array(pd.read_excel("t11-1-01.xlsx", sheet_name="Zeitreihe", skiprows=skiprows_data, usecols=usecols).columns)
#print(electric_cars)

values = electric_cars/allcars * 100

#make df with our data
df_BS_Electric_Cars = pd.DataFrame(columns=["INDICATOR_ID", "SPATIALUNIT_ID", "YEAR", "VALUE", "VALUE_ADDITION", "CAT"])
INDICATOR_ID = 997
SPATIALUNIT_ID = 1001
VALUE_ADDITION = np.nan
CAT = str(datetime.datetime.today().strftime('%d.%m.%y %H:%M'))
years = [2019, 2020]


df_BS_Electric_Cars['YEAR'] = years
df_BS_Electric_Cars['VALUE'] = values
df_BS_Electric_Cars['INDICATOR_ID'] = INDICATOR_ID
df_BS_Electric_Cars['SPATIALUNIT_ID'] = SPATIALUNIT_ID
df_BS_Electric_Cars['VALUE_ADDITION'] = VALUE_ADDITION
df_BS_Electric_Cars['CAT'] = CAT

print(df_BS_Electric_Cars)

# add data to "EN_INDICATORS_VALUES.csv"
export_file_name = os.path.join(credentials.local_path, credentials.local_file_name)
df_BS_Electric_Cars.to_csv(export_file_name, mode='a', header=False, index=False)

"""
996, Total new registrations of electric and hybrid motor cars [%] ,
Share of passenger cars (PW) with either electric or hybrid drive in all passenger cars put into circulation for the first time between October 1 of the previous year and September 30;
hybrid drive refers to all combinations of electric motor and combustion engine.
"""

years = [2019, 2020]

#get our data
skiprows_data_normal = [x for x in range(40) if x!=9]
skiprows_data_electric = [x for x in range(40) if x!=11]
usecols_1 = [x for x in range(12, 15)]
usecols_2 = [x for x in range(3, 12)]
values=[]
for year in years:
    data_row_1_normal = list(pd.read_excel("t11-1-03.xlsx", sheet_name=str(year - 1), skiprows=skiprows_data_normal, usecols=usecols_1).columns)
    data_row_2_normal = list(pd.read_excel("t11-1-03.xlsx", sheet_name=str(year), skiprows=skiprows_data_normal, usecols=usecols_2).columns)
    data_row_1_normal = [int(float(x)) for x in data_row_1_normal]
    data_row_2_normal = [int(float(x)) for x in data_row_2_normal]
    total_normal = np.sum(data_row_1_normal) + np.sum(data_row_2_normal)
    data_row_1_electric = list(pd.read_excel("t11-1-03.xlsx", sheet_name=str(year - 1), skiprows=skiprows_data_electric,usecols=usecols_1).columns)
    data_row_2_electric = list(pd.read_excel("t11-1-03.xlsx", sheet_name=str(year), skiprows=skiprows_data_electric, usecols=usecols_2).columns)
    data_row_1_electric = [int(float(x)) for x in data_row_1_electric]
    data_row_2_electric = [int(float(x)) for x in data_row_2_electric]
    total_electric = np.sum(data_row_1_electric + data_row_2_electric)
    value = total_electric/total_normal * 100
    values.append(value)


# make df with our data
df_BS_New_Electric_Cars = pd.DataFrame(columns=["INDICATOR_ID", "SPATIALUNIT_ID", "YEAR", "VALUE", "VALUE_ADDITION", "CAT"])
INDICATOR_ID = 996
SPATIALUNIT_ID = 1001
VALUE_ADDITION = np.nan
CAT = str(datetime.datetime.today().strftime('%d.%m.%y %H:%M'))

df_BS_New_Electric_Cars['YEAR'] = years
df_BS_New_Electric_Cars['VALUE'] = values
df_BS_New_Electric_Cars['INDICATOR_ID'] = INDICATOR_ID
df_BS_New_Electric_Cars['SPATIALUNIT_ID'] = SPATIALUNIT_ID
df_BS_New_Electric_Cars['VALUE_ADDITION'] = VALUE_ADDITION
df_BS_New_Electric_Cars['CAT'] = CAT

print(df_BS_New_Electric_Cars)

# add data to "EN_INDICATORS_VALUES.csv"
export_file_name = os.path.join(credentials.local_path, credentials.local_file_name)
df_BS_New_Electric_Cars.to_csv(export_file_name, mode='a', header=False, index=False)

""""
999,Charging stations of electronic cars [no.] ,Data taken from the Swiss Federal Office for Energy and converted to communes,,,,,,
998,Charging stations of electronic cars per 1000 inhabitants [no.] ,Data taken from the Swiss Federal Office for Energy and converted to communes,,,,,,
"""

# get data from: https://github.com/statistikZH/geocoords2spatialunits/blob/main/anzahl_ladestationen.csv, cantonal value: add values for Basel, Riehen and Bettingen
# population = 194840/1000, see above
number_of_stations = 63 + 2 + 2
number_of_stations_per_1000 = number_of_stations/population
values = [number_of_stations, number_of_stations_per_1000]

# create dataframe
df_BS_charging = pd.DataFrame(columns=["INDICATOR_ID", "SPATIALUNIT_ID", "YEAR", "VALUE", "VALUE_ADDITION", "CAT"])
INDICATOR_ID = [999, 998]
SPATIALUNIT_ID = 1001
VALUE_ADDITION = np.nan
CAT = str(datetime.datetime.today().strftime('%d.%m.%y %H:%M'))

df_BS_charging['YEAR'] = [2021, 2021]
df_BS_charging['VALUE'] = values
df_BS_charging['INDICATOR_ID'] = INDICATOR_ID
df_BS_charging['SPATIALUNIT_ID'] = SPATIALUNIT_ID
df_BS_charging['VALUE_ADDITION'] = VALUE_ADDITION
df_BS_charging['CAT'] = CAT

print(df_BS_charging['VALUE'])

# add data to "EN_INDICATORS_VALUES.csv"
export_file_name = os.path.join(credentials.local_path, credentials.local_file_name)
df_BS_charging.to_csv(export_file_name, mode='a', header=False, index=False)
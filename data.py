import numpy as np
import pandas as pd

# -----------------------------------------------------------------------------------------Loading CSV datasets
df_circuits = pd.read_csv("https://raw.githubusercontent.com/MiguelOva/F1_dash_final/main/data/circuits.csv")
df_constructor_results = pd.read_csv(
    'https://raw.githubusercontent.com/MiguelOva/F1_dash_final/main/data/constructor_results.csv')
df_constructor_standings = pd.read_csv(
    'https://raw.githubusercontent.com/MiguelOva/F1_dash_final/main/data/constructor_standings.csv')
df_constructors = pd.read_csv('https://raw.githubusercontent.com/MiguelOva/F1_dash_final/main/data/constructors.csv')
df_driver_standings = pd.read_csv(
    'https://raw.githubusercontent.com/MiguelOva/F1_dash_final/main/data/driver_standings.csv')
df_drivers = pd.read_csv('https://raw.githubusercontent.com/MiguelOva/F1_dash_final/main/data/drivers.csv')
df_lap_times = pd.read_csv('https://raw.githubusercontent.com/MiguelOva/F1_dash_final/main/data/lap_times.csv')
df_pit_stops = pd.read_csv('https://raw.githubusercontent.com/MiguelOva/F1_dash_final/main/data/pit_stops.csv')
df_qualifying = pd.read_csv('https://raw.githubusercontent.com/MiguelOva/F1_dash_final/main/data/qualifying.csv')
df_status = pd.read_csv('https://raw.githubusercontent.com/MiguelOva/F1_dash_final/main/data/status.csv')
df_seasons = pd.read_csv('https://raw.githubusercontent.com/MiguelOva/F1_dash_final/main/data/seasons.csv')
df_sprint_results = pd.read_csv('https://raw.githubusercontent.com/MiguelOva/F1_dash_final/main/data/sprint_results.csv')
df_results = pd.read_csv('https://raw.githubusercontent.com/MiguelOva/F1_dash_final/main/data/results.csv')
df_races = pd.read_csv('https://raw.githubusercontent.com/MiguelOva/F1_dash_final/main/data/races.csv')

# ------------------------------------------------------------------- TRACKS AND DATES
# Location Coordinates
df_coordinates = df_circuits.copy()
df_coordinates = df_coordinates[['circuitId', 'location', 'country', 'lat', 'lng']]
df_coordinates.drop_duplicates(inplace=True)
df_coordinates['circuitId'] = df_coordinates['circuitId'].astype(int)
df_coordinates['lat'] = df_coordinates['lat'].astype(float)
df_coordinates['lng'] = df_coordinates['lng'].astype(float)
# df_coordinates.head()
# df_coordinates.info()

# Races and Dates
df_races.drop(df_races.head(1).index, inplace=True)
df_races = df_races.reset_index(drop=True)
df_races['raceId'] = df_races['raceId'].astype(int)
df_races['year'] = df_races['year'].astype(int)
df_races['round'] = df_races['round'].astype(int)
df_races['circuitId'] = df_races['circuitId'].astype(int)
# df_races.head()
# df_races.info()

# Races, Dates and Coordinates
df_races = df_races.merge(df_coordinates, on='circuitId', how='left')
df_races = df_races.drop(['time', 'url'], axis=1)
df_races = df_races.rename(columns={'name': 'name_t'})
df_races["location_t"] = df_races["country"] + '-' + df_races["location"]
df_races = df_races[['circuitId', 'name_t', 'location_t', 'country', 'lat', 'lng', 'raceId', 'year', 'round']]

# Final Dataframe CIRCUITID, RACEID, and GEOLOCATION
# print(df_races)

# ------------------------------------------------------------------ NUMBER ROUNDS PER YEAR

number_rounds = df_races.loc[df_races.groupby('year')['round'].idxmax()]
number_rounds = number_rounds[['year', 'round']]
number_rounds = number_rounds.loc[number_rounds['year'] >= 2004]

# Final
# print(number_rounds)

# ------------------------------------------------------------------DRIVERS UNIQUE

# Full name
df_drivers["name_d"] = df_drivers["forename"] + ' ' + df_drivers["surname"]
df_drivers = df_drivers.rename(columns={'nationality': 'nationality_d'})

# choose desired columns
df_drivers = df_drivers[['driverId', 'code', 'name_d', 'nationality_d']]

# Substitute all \N with DNF
df_drivers['code'].loc[(df_drivers['code'].str.contains(r'^(?=.*N)'))] = 'Not Available'

# Final Dataframe DRIVERID, NAME, and NATIONALITY
# print(df_drivers)

# ------------------------------------------------------------------ CONSTRUCTORS UNIQUE

df_constructors = df_constructors.rename(columns={'name': 'name_c', 'nationality': 'nationality_c'})
df_constructors = df_constructors[['constructorId', 'name_c', 'nationality_c']]

# Final Dataframe constructorId, name_c, and nationality_c
# print(df_constructors)


# ------------------------------------------------------------------ STANDINGS DRIVER UNIQUE

df_dc = df_driver_standings.rename(columns={'points': 'champ_pts', 'position': 'champ_pos'})

df_dc = pd.merge(df_dc, df_drivers, how='inner', on=['driverId'])
df_dc = pd.merge(df_dc, df_races, how='inner', on=['raceId'])

df_dc = df_dc[['driverStandingsId', 'raceId', 'name_t', 'year', 'round',
               'driverId', 'code', 'name_d',
               'champ_pts', 'champ_pos', 'wins']]
# Final
# print(df_dc)

# ------------------------------------------------------------------ STANDINGS CHAMP UNIQUE

df_cc = df_constructor_standings.rename(columns={'points': 'champ_pts', 'position': 'champ_pos'})
df_cc.head()

df_cc = pd.merge(df_cc, df_constructors, how='inner', on=['constructorId'])
df_cc = pd.merge(df_cc, df_races, how='inner', on=['raceId'])

df_cc = df_cc[['constructorStandingsId', 'raceId', 'name_t', 'year', 'round',
               'constructorId', 'name_c',
               'champ_pts', 'champ_pos', 'wins']]

# Final
# print(df_cc)


# ------------------------------------------------------------------ RACES RESULTS

df_results_t = pd.merge(df_results, df_status, how='inner', on=['statusId'])
df_results_t = pd.merge(df_results_t, df_drivers, how='inner', on=['driverId'])
df_results_t = pd.merge(df_results_t, df_constructors, how='inner', on=['constructorId'])
df_results_t = pd.merge(df_results_t, df_races, how='inner', on=['raceId'])

# Dropping unnecessary columns
df_results_t = df_results_t.drop(['driverId', 'constructorId', 'circuitId', 'number', 'statusId',
                                  'location_t', 'lat', 'lng', 'positionText', 'code', 'time', 'milliseconds'], axis=1)

df_results_t['position'].loc[(df_results_t['position'].str.contains(r'^(?=.*N)'))] = 'DNF'
df_results_t = df_results_t.sort_values(by='year', ascending=False)

# Fastest lap // rank // fastestLapTime // fastestLapSpeed -- ONLY AVAILABLE AFTER "2004"

# Separate 1950-2003
dfr_old = df_results_t[df_results_t['year'] < 2004]
dfr_old = dfr_old.drop(['fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed'], axis=1)

# Substitute ALL /N WITH DNF
dfr_old['position'].loc[(dfr_old['position'].str.contains(r'^(?=.*N)'))] = 'DNF'

# Rearrange columns
old_columns = ['resultId', 'raceId', 'name_t', 'country', 'year', 'round', 'name_d',
               'nationality_d', 'grid', 'positionOrder', 'points', 'position', 'status', 'laps', 'name_c',
               'nationality_c']

dfr_old = dfr_old[old_columns]

# Final OLD
# print(dfr_old)


# Separate 2004-2021
dfr_new = df_results_t[df_results_t['year'] >= 2004]

# (we also don't have those stats for 2021 -- 12 -- Belgian GP - DROP -- RACEID -- 1063)
dfr_new = dfr_new[dfr_new.raceId != 1063]

# Substitute ALL /N WITH DNF
dfr_new['position'].loc[(dfr_new['position'].str.contains(r'^(?=.*N)'))] = 'DNF'
dfr_new['fastestLap'].loc[(dfr_new['fastestLap'].str.contains(r'^(?=.*N)'))] = 'DNF'
dfr_new['rank'].loc[(dfr_new['rank'].str.contains(r'^(?=.*N)'))] = 'DNF'
dfr_new['fastestLapTime'].loc[(dfr_new['fastestLapTime'].str.contains(r'^(?=.*N)'))] = 'DNF'
dfr_new['fastestLapSpeed'].loc[(dfr_new['fastestLapSpeed'].str.contains(r'^(?=.*N)'))] = 'DNF'

# Rearange Columns
new_columns = ['resultId', 'raceId', 'name_t', 'country', 'year', 'round', 'name_d', 'nationality_d',
               'grid', 'positionOrder', 'points', 'position', 'status', 'laps',
               'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed', 'name_c', 'nationality_c']

dfr_new = dfr_new[new_columns]

# Final Dataset
# print(dfr_new)

# ------------------------------------------------------------------ ALL PRIMARY TABLES
# ------------------------------------------------------------------ ALL PRIMARY TABLES
# ------------------------------------------------------------------ ALL PRIMARY TABLES
# ------------------------------------------------------------------ ALL PRIMARY TABLES
# ------------------------------------------------------------------ ALL PRIMARY TABLES
# ------------------------------------------------------------------ ALL PRIMARY TABLES

# TABLE CONTAINING DRIVERS NAMES AND CODES
# print("Drivers Table")
# print(df_drivers.head())
# print("\n")

# TABLE CONTAINING CONSTRUCTORS NAMES
# print("Constructors Table")
# print(df_constructors.head())
# print("\n")

# TABLE CONTAINING TRACK NAMES, YEAR, AND LOCATION
# print("Track, Years and Location Table")
# print(df_races.head())
# print("\n")

# TABLE CONTAINING CHAMPIONSHIP POINTS AND POSITION -- DRIVERS ONLY
# print("Championship Points and Positions -- Drivers")
# print(df_dc.head())
# print("\n")

# TABLE CONTAINING CHAMPIONSHIP POINTS AND POSITION -- CONSTRUCTORS ONLY
# print("Championship Points and Positions -- Constructors")
# print(df_cc.head())
# print("\n")

# TABLE CONTAINING RESULTS PARTICULAR RACE -- <<<<<< 2004
# print("Results for Races -- below 2004 - no speed")
# print(dfr_old.head())
# print("\n")

# TABLE CONTAINING RESULTS PARTICULAR RACE -- >>>>>> 2004
# print("Results for Races -- over 2004 - speed")
# print(dfr_new.head())
# print("\n")

# TABLE CONTAINING MAX ROUND PER YEAR
# print("Number of rounds per year")
# print(number_rounds.head())
# print("\n")

# --------------------------------------------------  HALL OF FAME
# --------------------------------------------------  HALL OF FAME
# --------------------------------------------------  HALL OF FAME

hall_of_fame = df_results_t.drop(['resultId','raceId','grid','laps','fastestLap','fastestLapTime','fastestLapSpeed'], axis=1)


# ------------------------------------------------------------------ OTHER TABLES
# ------------------------------------------------------------------ OTHER TABLES
# ------------------------------------------------------------------ OTHER TABLES

# Current
df_current = df_results_t[(df_results_t['year'] >= 2000) & (df_results_t['year'] <= 2021)]

# DRIVERS
total_points = df_current.groupby(['year', 'name_d'])['points'].sum().reset_index()

# TEAMS
total_points.rename(columns={'year': 'Year', 'name_d': 'Driver', 'points': 'Points'}, inplace=True)
total_points_team = df_current.groupby(['year', 'name_c'])['points'].sum().reset_index()
total_points_team.rename(columns={'year': 'Year', 'name_c': 'Team', 'points': 'Points'}, inplace=True)







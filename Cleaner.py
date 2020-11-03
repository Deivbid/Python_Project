import numpy as np
import pandas as pd
#Veamos la data que tenemos
df_20 = pd.read_csv('Data_Players/players_20.csv')
print(df_20.head())

#Dropear columnas que no me sirven (digo yo) para el estudio
cols = list(df_20.columns)
print(cols)
useless_columns = [
    'dob',
    'sofifa_id',
    'player_url',
    'long_name',
    'body_type',
    'real_face',
    'loaned_from',
    'nation_position',
    'nation_jersey_number'
]
df_20 = df_20.drop(useless_columns, axis=1)
print(df_20.head())

#Agregar una nueva columna Body Max Index
df_20['BMI'] = df_20['weight_kg'] / ((df_20['height_cm'] / 100)**2)
print(df_20.head())
print(df_20[['short_name', 'BMI']]) #Estos datos son reales y actualizados

#Deconstruir Player Positions
print("Tenemos Las siguientes positiones para cada jugador")

print(df_20[['short_name', 'player_positions']])
print('Obtenemos los dummies de cada posicion')

new_players_position = df_20['player_positions'].str.get_dummies(sep = ', ').add_prefix('Position_')
print('Nuestras nuevas columnas seran algo asi: ')

print(new_players_position.head())
print('Concatenamos todo: ')

df_20 = pd.concat([df_20, new_players_position], axis = 1)

#Limpiar procesar y asignar nuevos atributos a estas columnas 
columns = ['ls', 'st', 'rs', 'lw', 'lf', 'cf', 'rf', 'rw', 'lam', 'cam', 'ram',
       'lm', 'lcm', 'cm', 'rcm', 'rm', 'lwb', 'ldm', 'cdm', 'rdm', 'rwb', 'lb',
       'lcb', 'cb', 'rcb', 'rb']
print(df_20[columns].head())
new_ls_col = df_20['ls'].str.split('+', n = 1, expand = True) #Expand true returns a DF for us
print(new_ls_col)

for col in columns:
    df_20[col] = df_20[col].str.split('+', n = 1, expand = True)[0]

print(df_20[columns])

df_20[columns] = df_20[columns].fillna(0)
print(df_20[columns])
df_20[columns] = df_20[columns].astype(int)

#LLenar data faltante
missing_data = ["dribbling", "defending", "physic", "passing", "shooting", "pace"]
print(df_20[missing_data])

print('Cuantos NaN hay ???')
print(df_20[missing_data].isnull())
print(df_20[missing_data].isnull().sum())

for col in missing_data:
    df_20[missing_data] = df_20[missing_data].fillna(df_20[missing_data].median())

print(df_20[missing_data])


#limpiemos todo 
df_20 = df_20.fillna(0)
print(df_20.isnull().sum())






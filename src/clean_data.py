# This script generates the cleaned datasets for the 2019 and 2022 population Datasets and
# the economical data datset. It generates cleaned CSVs to be used in 'merge_data.py'.

import pandas as pd
import numpy as np

pop2019_info = pd.read_csv('data/raw/population2019_data_raw.csv', encoding='latin1')
pop2019_info.columns = ['canton', 'population_2015', 'population_2019', 'growth_%']
pop2019_info.drop(columns=['population_2015', 'growth_%'],inplace=True)
pop2019_info = pop2019_info.iloc[:-5]

new_canton_names = ['Sarapiqui', 'Garabito', 'Los Chiles', 'Carrillo', 'Talamanca',
                    'Parrita', 'La Cruz', 'Liberia', 'Santa Cruz', 'Guacimo', 'San Carlos',
                    'Bagaces', 'Quepos', 'Alajuelita', 'Esparza', 'Poas', 'Orotina',
                    'Pococi', 'Barva', 'Puntarenas', 'Santa Barbara', 'Upala', 'Alajuela',
                    'Santa Ana', 'San Rafael', 'Buenos Aires', 'Turrubares', 'Guatuso',
                    'Matina', 'Flores', 'Palmares', 'Canas', 'Golfito', 'San Ramon',
                    'Corredores', 'Heredia', 'Zarcero', 'Naranjo', 'Sarchi',
                    'San Isidro', 'La Union', 'Leon Cortes Castro', 'Atenas', 'Vazquez de Coronado',
                    'Montes de Oro', 'San Mateo', 'Nicoya', 'Desamparados', 'Escazu',
                    'Santo Domingo', 'Goicoechea', 'Puriscal', 'Aserri', 'Belen', 'Mora',
                    'El Guarco', 'Tarrazu', 'Curridabat', 'Paraiso', 'Oreamuno', 'Tibas',
                    'Cartago', 'San Jose', 'Abangares', 'Alvarado', 'Acosta', 'Dota',
                    'Siquirres', 'San Pablo', 'Tilaran', 'Moravia', 'Hojancha', 'Osa',
                    'Limon', 'Montes de Oca', 'Nandayure', 'Jimenez', 'Coto Brus',
                    'Perez Zeledon', 'Turrialba', 'Rio Cuarto', 'Grecia']

pop2019_info['canton'] = new_canton_names
pop2019_info['population_2019'] = pop2019_info['population_2019'].astype(int)
pop2019_info.to_csv('data/cleaned/population2019_clean.csv', index=False)

#########################################################################################

pop2022_info = pd.read_csv('data/raw/population2022_data_raw.csv', encoding='latin1')
pop2022_info.rename(columns={'Cantón': 'canton'},inplace=True)
pop2022_info.rename(columns={'2022': 'population_2022'},inplace=True)

pop2022_info.drop(columns=['1973', '1984', '2000', '2011'],inplace=True)
pop2022_info.drop(pop2022_info.index[0], inplace=True)

pop2022_info['canton'] = (pop2022_info['canton'].str.normalize('NFKD').str.encode(
    'ascii', errors='ignore').str.decode('utf-8'))

pop2022_info = pop2022_info.replace('Leon Cortes', 'Leon Cortes Castro')
pop2022_info.to_csv('data/cleaned/population2022_clean.csv', index=False)

##########################################################################################

econ_info = pd.read_csv('data/raw/economic_data_raw.csv',encoding='latin1',thousands=',',
                        na_values=[' -   ', '-', ''], skipinitialspace=True)
econ_info.columns = ['year', 'region', 'province_code', 'province', 'canton_code',
                    'canton', 'added_value', 'product_tax', 'gdp', 'exports', 'imports']

text_columns = ['region', 'province_code', 'province', 'canton_code', 'canton']
num_columns = ['year', 'added_value', 'product_tax', 'gdp', 'exports', 'imports']

econ_info[text_columns] = econ_info[text_columns].apply(lambda x: (x.astype(str).str.strip()
                        .str.normalize('NFKD').str.encode('ascii',errors='ignore')
                        .str.decode('utf-8')))

for col in num_columns:
    econ_info[col] = (econ_info[col].astype(str).str.replace(',', '', regex=False)
                      .str.strip())
    econ_info[col] = pd.to_numeric(econ_info[col], errors='coerce')

econ_info[num_columns] = econ_info[num_columns].fillna(0)

econ_info.drop(econ_info[econ_info['year'].isin([2020, 2021])].index, inplace=True)

econ_info.replace({'Monteverde': 'Puntarenas', 'Puerto Jimenez': 'Golfito'}, inplace=True)

df_2022 = econ_info[econ_info['year'] == 2022]
df_2019 = econ_info[econ_info['year'] == 2019]

df_2022_agg = (df_2022.groupby(['year', 'canton'], as_index=False)
    .agg({'region': 'first','province_code': 'first','province': 'first',
            'canton_code': 'first', 'added_value': 'sum','product_tax': 'sum','gdp': 'sum',
            'exports': 'sum','imports': 'sum'}))

econ_info = pd.concat([df_2019, df_2022_agg], ignore_index=True)

econ_info = econ_info.sort_values(['year', 'canton'])

econ_info.to_csv('data/cleaned/economic_clean.csv', index=False)
#print(econ_info.head())
#print(econ_info.info())
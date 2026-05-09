# This script cleans, formats and transforms the 2019 and 2022 population datasets, along with the economic indicators dataset after
# extracting the data from them. It outputs cleaned CSVs to be used in 'merge_data.py'.

import pandas as pd

def normalize_text_columns(df, columns):
    df[columns] = df[columns].apply(
        lambda x: (
            x.astype(str)
             .str.strip()
             .str.normalize('NFKD')
             .str.encode('ascii', errors='ignore')
             .str.decode('utf-8')
        )
    )
    return df

#Extraction and EDA of the 2019 canton population dataset.
pop2019_info = pd.read_csv('data/raw/population2019_data_raw.csv', encoding='latin1')
print(pop2019_info.head())
print(pop2019_info.info())

#Cleaning/transforming 2019 population dataset.
pop2019_info.columns = ['canton', 'population_2015', 'population_2019', 'growth_%']
pop2019_info.drop(columns=['population_2015', 'growth_%'],inplace=True)
pop2019_info = pop2019_info.iloc[:-5]

#Not the cleanest option. If possible, renaming the canton rows could be better done at source.
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

text_columns = ['canton']
pop2019_info = normalize_text_columns(pop2019_info, text_columns)

pop2019_info.to_csv('data/cleaned/population2019_clean.csv', index=False)

#Extraction and EDA of the 2022 canton population dataset.
pop2022_info = pd.read_csv('data/raw/population2022_data_raw.csv', encoding='latin1')
print(pop2022_info.head())
print(pop2022_info.info())

#Cleaning/transforming 2022 population dataset.
pop2022_info.rename(columns={'Cantón': 'canton'},inplace=True)
pop2022_info.rename(columns={'2022': 'population_2022'},inplace=True)

pop2022_info.drop(columns=['1973', '1984', '2000', '2011'],inplace=True)
pop2022_info.drop(pop2022_info.index[0], inplace=True)

text_columns = ['canton']
pop2022_info = normalize_text_columns(pop2022_info, text_columns)

#Correction on a canton name.
pop2022_info.replace('Leon Cortes', 'Leon Cortes Castro', inplace= True)

pop2022_info.to_csv('data/cleaned/population2022_clean.csv', index=False)

#Extraction and EDA of the economic indicators dataset.
econ_info = pd.read_csv('data/raw/economic_data_raw.csv',encoding='latin1',thousands=',',
                        na_values=[' -   ', '-', ''], skipinitialspace=True)
print(econ_info.head())
print(econ_info.info())

#Cleaning/transforming the economic indicators dataset.
econ_info.columns = ['year', 'region', 'prov_code', 'province', 'can_code',
                    'canton', 'added_value', 'product_tax', 'gdp', 'exports', 'imports']

text_columns = ['region', 'prov_code', 'province', 'can_code', 'canton']
num_columns = ['year', 'added_value', 'product_tax', 'gdp', 'exports', 'imports']

econ_info = normalize_text_columns(econ_info, text_columns)

for col in num_columns:
    econ_info[col] = (econ_info[col].astype(str).str.replace(',', '', regex=False)
                      .str.strip())
    econ_info[col] = pd.to_numeric(econ_info[col], errors='coerce')

econ_info[num_columns] = econ_info[num_columns].fillna(0)

#Based on project objectives, only 2019 and 2022 data is required
econ_info.drop(econ_info[econ_info['year'].isin([2020, 2021])].index, inplace=True)

#Two new "cantones" were created during the 2021-2022 period. Their data was aggregated with the data of the "cantones" they were
#part of before.
econ_info['canton'] = econ_info['canton'].replace({'Monteverde': 'Puntarenas', 'Puerto Jimenez': 'Golfito'})

df_2022 = econ_info[econ_info['year'] == 2022]
df_2019 = econ_info[econ_info['year'] == 2019]

#Aggregating data from Monteverde into Puntarenas, and Puerto Jimenez into Golfito.
df_2022_agg = (df_2022.groupby(['year', 'canton'], as_index=False)
    .agg({'region': 'first','prov_code': 'first','province': 'first',
            'can_code': 'first', 'added_value': 'sum','product_tax': 'sum','gdp': 'sum',
            'exports': 'sum','imports': 'sum'}))

econ_info = pd.concat([df_2019, df_2022_agg], ignore_index=True)

econ_info = econ_info.sort_values(['year', 'canton'])

econ_info.to_csv('data/cleaned/economic_clean.csv', index=False)
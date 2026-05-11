#This script cleans, formats and transforms the 2019 and 2022 population datasets, along with the economic indicators dataset after
#extracting the data from them. It outputs cleaned CSVs to be used in 'merge_data.py'.

import pandas as pd

#Defining a function that will clean text columns: normalizing white spaces, separating 'de' and 'del' from
#place names, separating CamelCase and removing accents. 
def normalize_text_columns(df, columns):

    def clean_text(series):
        return (
            series.astype(str)
            .str.strip()
            .str.normalize('NFKD')
            .str.encode('ascii', errors='ignore')
            .str.decode('utf-8')
            .str.replace(r'([a-z])([A-Z])', r'\1 \2', regex=True)
            .str.replace('de ', ' de ', regex=False)
            .str.replace('del ', ' del ', regex=False)
            .str.replace(r'[^A-Za-z\s]', '', regex=True)
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
        )

    df[columns] = df[columns].apply(clean_text)

    return df

#Extraction and EDA of the raw 2019 canton population dataset.
pop2019_info = pd.read_csv('data/raw/population2019_data_raw.csv', encoding='utf-8')
print(pop2019_info.head())
print(pop2019_info.info())

#Cleaning/transforming 2019 population dataset.
pop2019_info.columns = ['canton', 'population_2015', 'population_2019', 'growth_%']
pop2019_info.drop(columns=['population_2015', 'growth_%'],inplace=True)
pop2019_info = pop2019_info.iloc[:-5]

text_columns = ['canton']

pop2019_info = normalize_text_columns(pop2019_info, text_columns)
pop2019_info['canton'] = pop2019_info['canton'].replace({'Valver de Vega': 'Sarchi',
                                                         'Leon Cortes': 'Leon Cortes Castro',
                                                         'Vasquez de Coronado': 'Vazquez de Coronado'})

pop2019_info['population_2019'] = pop2019_info['population_2019'].astype(int)

pop2019_info.to_csv('data/cleaned/population2019_clean.csv', index=False)

#Extraction and EDA of the raw 2022 canton population dataset.
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

#Extraction and EDA of the raw economic indicators dataset.
econ_info = pd.read_csv('data/raw/economic_data_raw.csv',encoding='latin1',thousands=',',
                        na_values=[' -   ', '-', ''], skipinitialspace=True)
print(econ_info.head())
print(econ_info.info())

#Cleaning/transforming the economic indicators dataset.
econ_info.columns = ['year', 'region', 'prov_code', 'province', 'can_code',
                    'canton', 'added_value', 'product_tax', 'gdp', 'exports', 'imports']

text_columns = ['region', 'province', 'canton']
num_columns = ['year', 'prov_code', 'can_code', 'added_value', 'product_tax', 'gdp', 'exports', 'imports']

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
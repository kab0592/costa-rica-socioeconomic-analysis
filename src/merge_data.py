#This script merges the cleaned datasets for 2019 and 2022 population, and for economic indicators. The data is transformed into a
#consolidated dataset which combines economic indicators and population by canton, for both 2019 and 2022. It outputs a CSV to be
#used in 'analyze_data.py'.

import pandas as pd

pop2019 = pd.read_csv('data/cleaned/population2019_clean.csv')
pop2022 = pd.read_csv('data/cleaned/population2022_clean.csv')
econ_data = pd.read_csv('data/cleaned/economic_clean.csv')

def validate_merge(df, subset_columns):
    assert not df.duplicated(subset=subset_columns).any()
    assert df.isna().sum().sum() == 0

econ_data_2019 = econ_data[econ_data['year'] == 2019].drop(['added_value', 'product_tax'], axis=1)
econ_data_2022 = econ_data[econ_data['year'] == 2022].drop(['added_value', 'product_tax'], axis=1)

#Merging data from population and economic indicators datasets
merged_2019 = econ_data_2019.merge(pop2019, on='canton')
merged_2019 = merged_2019.rename(columns={'population_2019': 'population'})
merged_2022 = econ_data_2022.merge(pop2022, on='canton')
merged_2022 = merged_2022.rename(columns={'population_2022': 'population'})

socioeconomic_cr = pd.concat([merged_2019, merged_2022], ignore_index=True)
validate_merge(socioeconomic_cr, ['canton', 'year'])
socioeconomic_cr.to_csv('data/processed/socioeconomic_merged_complete.csv', index=False)
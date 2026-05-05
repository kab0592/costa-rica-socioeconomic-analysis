import pandas as pd

pop2019 = pd.read_csv('data/cleaned/population2019_clean.csv')
pop2022 = pd.read_csv('data/cleaned/population2022_clean.csv')
econ_data = pd.read_csv('data/cleaned/economic_clean.csv')

econ_data_2019 = econ_data[econ_data['year'] == 2019]
econ_data_2022 = econ_data[econ_data['year'] == 2022]

merged_2019 = econ_data_2019.merge(pop2019, on='canton')
merged_2019 = merged_2019.rename(columns={'population_2019': 'population'})

merged_2022 = econ_data_2022.merge(pop2022, on='canton')
merged_2022 = merged_2022.rename(columns={'population_2022': 'population'})

socioeconomic_cr = pd.concat([merged_2019, merged_2022], ignore_index=True)

metrics = {"gdp_pc": lambda df: df["gdp"] / df["population"], "exports_pc": lambda df: df["exports"] / df["population"], 
           "imports_pc": lambda df: df["imports"] / df["population"], "trade_balance": lambda df: df["exports"] - df["imports"]}

for name, func in metrics.items():
    socioeconomic_cr[name] = func(socioeconomic_cr)

socioeconomic_cr.to_csv('data/processed/socioeconomic_merged_complete.csv', index=False)

socioeconomic_cr_2019 = socioeconomic_cr[socioeconomic_cr['year'] == 2019]
socioeconomic_cr_2022 = socioeconomic_cr[socioeconomic_cr['year'] == 2022]

socioeconomic_analysis = socioeconomic_cr_2022.merge(socioeconomic_cr_2019[['canton','gdp', 'exports', 'imports']], on= 'canton')
socioeconomic_analysis = socioeconomic_analysis.rename(columns={'gdp_x': 'gdp_2022', 'exports_x': 'exports_2022', 
                                                       'imports_x': 'imports_2022', 'gdp_y': 'gdp_2019', 'exports_y': 'exports_2019', 
                                                       'imports_y': 'imports_2019'})

metrics = {"gdp_growth": lambda df: (df["gdp_2022"] - df["gdp_2019"]) / df["gdp_2019"],
           "exports_growth": lambda df: (df["exports_2022"] - df["gdp_2019"]) / df["gdp_2019"], 
           "imports_growth": lambda df: (df["imports_2022"] - df["imports_2019"]) / df["imports_2019"]}

for name, func in metrics.items():
    socioeconomic_analysis[name] = func(socioeconomic_analysis)

socioeconomic_analysis["gdp_growth_cat"] = socioeconomic_analysis["gdp_growth"].apply(lambda x:
                                                                                      "Strong" if x > 0.04 else ("Moderate" if 0.02 < x < 0.03
                                                                                        else ("Slow" if 0 < x < 0.02 else "Recession")))

socioeconomic_analysis.to_csv('data/processed/socioeconomic_merged_2022.csv', index=False)
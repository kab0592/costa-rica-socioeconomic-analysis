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

metrics = {"gdp_pc": lambda df: df["gdp"] / df["population"], "trade_balance": lambda df: df["exports"] - df["imports"]}

for name, func in metrics.items():
    socioeconomic_cr[name] = func(socioeconomic_cr)

socioeconomic_cr.to_csv('data/processed/socioeconomic_merged_complete.csv', index=False)

socioeconomic_cr_2019 = socioeconomic_cr[socioeconomic_cr['year'] == 2019]
socioeconomic_cr_2022 = socioeconomic_cr[socioeconomic_cr['year'] == 2022]

socioeconomic_analysis = socioeconomic_cr_2022.merge(socioeconomic_cr_2019[['canton','gdp', 'population', 'exports', 'imports', 'gdp_pc']],
                                                     on= 'canton')
socioeconomic_analysis = socioeconomic_analysis.rename(columns={'gdp_x': 'gdp', 'exports_x': 'exports', 'population_x': 'population',
                                                       'imports_x': 'imports', 'trade_balance_x': 'trade_balance', 'gdp_pc_x': 'gdp_pc',
                                                       'gdp_y': 'gdp_2019', 'exports_y': 'exports_2019', 'imports_y': 'imports_2019',
                                                       'population_y': 'population_2019', 'gdp_pc_y': 'gdp_pc_2019'})

initial_year = 2019
final_year = 2022
growth_periods = final_year - initial_year

metrics = {"gdp_cagr": lambda df: (((df["gdp"] / df["gdp_2019"]) ** (1/growth_periods)) - 1),
           "gdp_pc_cagr": lambda df: (((df["gdp_pc"] / df["gdp_pc_2019"]) ** (1/growth_periods)) - 1), 
           "exports_cagr": lambda df: (((df["exports"] / df["exports_2019"]) ** (1/growth_periods)) - 1),
           "imports_cagr": lambda df: (((df["imports"] / df["imports_2019"]) ** (1/growth_periods)) - 1),
           "population_cagr": lambda df: (((df["population"] / df["population_2019"]) ** (1/growth_periods)) - 1)}

for name, func in metrics.items():
    socioeconomic_analysis[name] = func(socioeconomic_analysis)

def classify_growth(x):
    if x < 0:
        return "Recession"
    elif x < 0.02:
        return "Slow"
    elif x < 0.04:
        return "Moderate"
    else:
        return "Strong"

socioeconomic_analysis["gdp_cagr_cat"] = (socioeconomic_analysis["gdp_cagr"].apply(classify_growth))

socioeconomic_analysis["gdp_pc_cagr_cat"] = (socioeconomic_analysis["gdp_pc_cagr"].apply(classify_growth))

socioeconomic_analysis.to_csv('data/processed/socioeconomic_merged_2022.csv', index=False)
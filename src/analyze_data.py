#This script uses the consolidated dataset with 2019/2022 population and economic indicators. The data is transformed and filtered
#to only include 2022 data for this specific analysis (along some key 2019 data for growth-related metrics). Feature engineering is
#performed to add additional economic indicators. It outputs a CSV to be loaded in analytical or visualization tools.

import pandas as pd

socioeconomic_cr = pd.read_csv('data/processed/socioeconomic_merged_complete.csv')

def validate_merge(df, key_column):
    assert df[key_column].is_unique
    assert df.isna().sum().sum() == 0

socioeconomic_cr_2019 = socioeconomic_cr[socioeconomic_cr['year'] == 2019]
socioeconomic_cr_2022 = socioeconomic_cr[socioeconomic_cr['year'] == 2022]

socioeconomic_analysis = socioeconomic_cr_2022.merge(socioeconomic_cr_2019[['gdp', 'population', 'exports', 'imports', 'canton']],
                                                     on= 'canton',suffixes = ('','_2019'))
validate_merge(socioeconomic_analysis, 'canton')

metrics = {"gdp_pc": lambda df: df["gdp"] / df["population"], "trade_balance": lambda df: df["exports"] - df["imports"],
           "gdp_pc_2019": lambda df: df["gdp_2019"] / df["population_2019"]}

for name, func in metrics.items():
    socioeconomic_analysis[name] = func(socioeconomic_analysis)

#CAGR metrics calculation.
initial_year = 2019
final_year = 2022
growth_periods = final_year - initial_year

def calculate_cagr(current, previous, periods):
    return ((current / previous) ** (1 / periods)) - 1

socioeconomic_analysis["gdp_cagr"] = calculate_cagr(socioeconomic_analysis["gdp"], socioeconomic_analysis["gdp_2019"], growth_periods)
socioeconomic_analysis["gdp_pc_cagr"] = calculate_cagr(socioeconomic_analysis["gdp_pc"], socioeconomic_analysis["gdp_pc_2019"], growth_periods)
socioeconomic_analysis["population_cagr"] = calculate_cagr(socioeconomic_analysis["population"], socioeconomic_analysis["population_2019"], growth_periods)

#Growth classification metrics.
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

#Growth type metrics.
def type_growth(x, y):
    if x > 0 and y > 0:
        return "Inclusive"
    elif x > 0 and y <= 0:
        return "Population-driven"
    elif x <= 0 and y > 0:
        return "Efficiency Gain"
    else:
        return "Decline"

socioeconomic_analysis['growth_type'] = (socioeconomic_analysis.apply(lambda row: type_growth(row['gdp_cagr'], row['gdp_pc_cagr']),
                                                                      axis=1))

socioeconomic_analysis.to_csv('data/processed/socioeconomic_analysis.csv', index=False)
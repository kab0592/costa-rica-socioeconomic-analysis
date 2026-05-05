# This script opens the CSV files with data from official sources. It allows to review the
# columns and the first rows of data. After this, the data is opened # and cleaned with
# 'clean_data/py'.

import pandas as pd

econ_info = pd.read_csv("data/raw/economic_data_raw.csv", encoding="latin1")
pop2019_info = pd.read_csv("data/raw/population2019_data_raw.csv", encoding="latin1")
pop2022_info = pd.read_csv("data/raw/population2022_data_raw.csv", encoding="latin1")

print("##################################econ_info################################")
print(econ_info.head())
print(econ_info.info())
print("###############################pop2019_info################################")
print(pop2019_info.head())
print(pop2019_info.info())
print("###############################pop2022_info################################")
print(pop2022_info.head())
print(pop2022_info.info())
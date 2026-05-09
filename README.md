# Costa Rica Socioeconomic Analysis by *Canton* (2019–2022)

## Project Overview

This project analyzes and compares socioeconomic data for Costa Rican *cantones* between 2019 and 2022. The project showcases the use of Python (Pandas), Excel, QGIS and Power BI within a complete data analysis workflow.

## Project Objective

Compare and contrast the socioeconomic situation of Costa Rican *cantones* in 2019 and 2022, to evaluate the impact of the COVID-19 pandemic on key economic indicators.

## Data Sources and Overview

- INEC (Instituto Nacional de Estadística y Censos): Population data
- BCCR (Banco Central de Costa Rica): Economic data
- SNIT (Sistema Nacional de Informacion Territorial): *Cantones* geospatial boundaries

### Main datasets
- Population estimates (2019)
- Population census (2022)
- Economic indicators dataset

### Key variables
- GDP
- Population
- GDP per capita
- CAGR metrics
- Growth category and growth type

## Methodology and workflow

1. Raw data ingestion

The files found in `data/raw` were ingested with `clean_data.py`.

2. Initial exploratory data analysis (EDA)

Using `clean_data.py`, the data was extracted and transformed into Pandas dataframes, allowing exploratory analysis to identify required cleaning and transformation steps. 

3. Data cleaning and normalization

The datasets were cleaned, standardized, and transformed into an appropriate input for `merge_data.py`.

4. Dataset merging

Using `merge_data.py`, one dataset including population data and economic indicators for each *canton* in two specific years (2019 and 2022) was consolidated.

5. Feature engineering

Using `analyze_data.py`, a final dataframe was created, which includes the key economic indicators for both 2019 and 2022. After this, feature engineering was performed to develop some additional metrics for study. A more detailed look of the engineered features can be seen below. This final dataset (`socioeconomic_analysis.csv`) is consolidated and ready to be loaded into an analysis or visualization tool.

6. Dashboard creation

The consolidated dataset (`socioeconomic_analysis.csv`) is loaded in PowerBi Desktop to create visualizations. Power Query was used to validate data types and confirm that the dataset was ready for visualization..

7. Insight generation

#*************************

### Engineered Features
| Feature | Comments |
|---|---|
| GDP per capita | GDP was normalized with population to have a more comparable view of the metric in the two specific years. |
| Trade balance | Used to see the dynamics of trade within the *canton* for 2022. |
| CAGR (various metrics) | CAGR metrics were chosen to further normalize the data and to annualize changes between non-consecutive years (2019–2022), instead of using a standard raw growth metric. CAGR metrics were calculated for GDP, GDP per capita and population. CAGR is defined by `CAGR = (Final Value / Initial Value)^(1 / Years) - 1`|
| Growth classification | Growth categories were defined using conventions commonly found in macroeconomic and financial analysis literature (International Monetary Fund (2024). *World Economic Outlook: Navigating Global Divergences*.). Following this, if the CAGR is over 4%, the growth is defined as 'Strong'. If the value is between 2 and 4%, it is considered 'Moderate'. A growth between 0 and 2% is considered 'Slow'; and one under 0% is considered 'Recession'. |
| Growth type | This nominal metric was also based on the interpretation of conventions found in literature (Barro, R. J., and Sala-i-Martin, X. (2004). *Economic Growth* (2nd ed.)) to make a distinction between scale growth and welfare-adjusted growth. According to this, growth in both CAGR GDP and CAGR GDP per capita is 'Inclusive'. If CAGR GDP grows but CAGR GDP per capita decreases, the growth is 'Population-driven'. If CAGR GDP decreases but CAGR GDP per capita grows, it is considered 'Efficiency gain'. Lastly, a decrease in both features represents a 'Decline'.|

## Tools Used

- Python (Pandas)
- Power BI
- QGIS
- Excel
- Git/GitHub
- Visual Studio Code

## How to Run

```bash
python src/clean_data.py
python src/merge_data.py
python src/analyze_data.py
```

## Folder structure

#**************

## Data Limitations

*******************
Very important section.

I strongly recommend you include:

boundary harmonization,
limited temporal coverage,
nominal GDP limitations,
post-pandemic distortion effects.

Example topics:

Monteverde/Puerto Jiménez administrative harmonization
Only two temporal snapshots
Inflation not adjusted
Census vs estimate population mismatch

This adds analytical maturity.
****************************

## Visualizations

### Dashboard
Power BI dashboard includes:
- Choropleth map of *cantones* by growth type
- CAGR GDP vs CAGR GDP per capita scatter plot
- Ranked bar graph for *cantones* with higher CAGR GDP per capita
- Ranked bar graph for *cantones* with lower CAGR GDP per capita

#********** ADD SCREENSHOTS

## Key Insights

aaaaaaaaa
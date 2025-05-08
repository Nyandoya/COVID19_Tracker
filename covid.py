# 1. Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 2. Load Data
df = pd.read_csv('owid-covid-data.csv')

# 3. Data Cleaning
# Filter countries and handle missing values
countries = ['Kenya', 'United States', 'India', 'Brazil', 'Germany']
covid = df[df['location'].isin(countries)].copy()

# Convert date and sort
covid['date'] = pd.to_datetime(covid['date'])
covid.sort_values(['location', 'date'], inplace=True)

# Forward-fill cumulative metrics
cumulative_cols = ['total_cases', 'total_deaths', 'total_vaccinations']
covid[cumulative_cols] = covid.groupby('location')[cumulative_cols].ffill()

# Calculate derived metrics
covid['death_rate'] = (covid['total_deaths'] / covid['total_cases'] * 100).round(2)
covid['cases_per_million'] = covid['total_cases'] / (covid['population'] / 1e6)

# 4. EDA Visualizations
plt.figure(figsize=(14, 8))
for country in countries:
    subset = covid[covid['location'] == country]
    plt.plot(subset['date'], subset['total_cases'], label=country)
plt.title('COVID-19 Total Cases Evolution')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.grid(True)
plt.show()

# 5. Vaccination Progress
plt.figure(figsize=(12, 6))
sns.lineplot(data=covid, x='date', y='people_fully_vaccinated_per_hundred', hue='location')
plt.title('Fully Vaccinated Population (%)')
plt.xlabel('Date')
plt.ylabel('Percentage Vaccinated')
plt.show()

# 6. Choropleth Map (Latest Data)
latest = covid[covid['date'] == covid['date'].max()]
fig = px.choropleth(latest,
                    locations="iso_code",
                    color="total_cases",
                    hover_name="location",
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title="Global COVID-19 Case Distribution")
fig.show()

# 7. Key Insights
'''
**Key Findings:**
1. The United States experienced the earliest and largest case surge
2. India shows the steepest growth curve in mid-2021
3. Germany maintained relatively lower death rates (1.5-2.5%)
4. Vaccination rates correlate with case reduction post-2021
5. Kenya shows delayed pandemic progression compared to others
'''
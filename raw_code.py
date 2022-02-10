# ===================================
# ===================================
# Copyright (c) 2022 Harsh Mehta (gonewithharshwinds)
# ===================================
# Covid-19-Data-Analysis-Project-by-gonewithharshwinds
# ===================================
# Author : Harsh Mehta
# Date : Thu 10 Feb 5:06 pm, 2022
# ===================================
# ===================================


# for data analysis
import pandas as pn
# for math
import numpy as np
# for plotting
import matplotlib.pyplot as mpl
import seaborn as sns
import plotly.express as xp
from plotly.subplots import make_subplots
# for date and time
from datetime import datetime

# import files
covid_df =pn.read_csv("/Users/gonewithharshwinds/.../covid_19_india.csv")
vaccine_df = pn.read_csv("/Users/gonewithharshwinds/.../covid_vaccine_statewise.csv")

# removing unnecessary data
covid_df.drop(["Sno", "Time", "ConfirmedIndianNational", "ConfirmedForeignNational"], inplace = True, axis = 1)

# to assign proper date format
covid_df['Date'] = pn.to_datetime(covid_df['Date'], format = '%Y-%m-%d')

# print active cases in India
covid_df['ActiveCases'] = covid_df['Confirmed'] - (covid_df['Cured'] + covid_df['Deaths'])

# create pivot table using pandas - summing confirmed & cured cases for each states & ut
statewise = pn.pivot_table(covid_df, values = ["Confirmed", "Deaths", "Cured"], index = "State/UnionTerritory", aggfunc = max)

# recovery rate (Cured/Confirmed)*100
statewise["RecoveryRate"] = statewise["Cured"]*100/statewise["Confirmed"]

# mortality rate (Deaths/Confirmed)*100
statewise["MortalityRate"] = statewise["Deaths"]*100/statewise["Confirmed"]

# print table with design
statewise = statewise.sort_values(by = "Confirmed", ascending = False)
statewise.style.background_gradient(cmap = "copper")

-----

# top 10 states with most active cases
top_10_active_states_cases = covid_df.groupby(by = 'State/UnionTerritory').max()[['ActiveCases' , 'Date']].sort_values(by = ['ActiveCases'], ascending = False).reset_index()
fig = mpl.figure(figsize=(16,9))
mpl.title("Top 10 states with most Active Cases in India", size = 25)
ax = sns.barplot(data = top_10_active_states_cases.iloc[:10], y = "ActiveCases", x = "State/UnionTerritory", linewidth = 1.5, edgecolor = 'green')

mpl.xlabel("States")
mpl.ylabel("Total Active Cases")
mpl.show()

-----

# top 10 states with most death cases
top_10_death_states_cases = covid_df.groupby(by = 'State/UnionTerritory').max()[['Deaths' , 'Date']].sort_values(by = ['Deaths'], ascending = False).reset_index()
fig = mpl.figure(figsize=(18, 5))
mpl.title("Top 10 states with most Death Cases in India", size = 25)
ax = sns.barplot(data = top_10_death_states_cases.iloc[:12], y = "Deaths", x = "State/UnionTerritory", linewidth = 1.5, edgecolor = 'red')

mpl.xlabel("States")
mpl.ylabel("Total Death Cases")
mpl.show()

-----

# Growth Trend in states
fig = mpl.figure(figsize = (12,6))

ax = sns.lineplot(data = covid_df[covid_df['State/UnionTerritory'].isin(['Maharashtra', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Uttar Pradesh'])], x = 'Date', y = 'ActiveCases', hue = 'State/UnionTerritory')
ax.set_title("Top 5 Affected States in India", size=16)


# renaming updated on to vaccination date
vaccine_df.rename(columns = {'Updated On' : 'Vaccination_date'}, inplace = True)
vaccine_df.head()

# identify null & process out unnecessary data
vaccine_df.isnull().sum()
vaccination = vaccine_df.drop(columns = ['Sputnik V (Doses Administered)', 'AEFI', '18-44 Years (Doses Administered)', '45-60 Years (Doses Administered)', '60+ Years (Doses Administered)'], axis = 1)

# Male & Female vaccination
male = vaccination["Male(Individuals Vaccinated)"].sum()
female= vaccination["Female(Individuals Vaccinated)"].sum()
xp.pie(names=["Male", "Female"], values = [male, female], title = "Male & Female Vaccination")

# Remove rows where state is India
vaccine = vaccine_df[vaccine_df.State!="India"]

# Rename Total Individuals Vaccinated to Total
vaccine.rename(columns = {"Total Individuals Vaccinated" : "Total"}, inplace = True)

-----

# Most Vaccinated State
max_vac = vaccine.groupby('State')['Total'].sum().to_frame('Total')
max_vac = max_vac.sort_values('Total', ascending = False)[:5]
max_vac

fig = mpl.figure(figsize = (10,5))
mpl.title("Top 5 vaccinated States in India", size = 20)
x = sns.barplot(data= max_vac.iloc[:10], y = max_vac.Total, x = max_vac.index, linewidth = 1.5, edgecolor = 'blue')

mpl.xlabel("States")
mpl.ylabel("Vaccination")
mpl.show()

-----

# Least Vaccinated State

min_vac = vaccine.groupby('State')['Total'].sum().to_frame('Total')
min_vac = min_vac.sort_values('Total', ascending = True)[:5]
min_vac

fig = mpl.figure(figsize = (16,5))
mpl.title("Bottom 5 vaccinated States in India", size = 25)
x = sns.barplot(data= min_vac.iloc[:10], y = min_vac.Total, x = min_vac.index, linewidth = 1.5, edgecolor = 'pink')

mpl.xlabel("States")
mpl.ylabel("Vaccination")
mpl.show()

# ===================================

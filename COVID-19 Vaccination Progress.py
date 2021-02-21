#!/usr/bin/env python
# coding: utf-8

# # <p style="text-align: center;">COVID-19 World Vaccination Progress </p>

# ### Problem Definition

# Covid-19 pandemic has been a challenge with over hundred million cases and over two million deaths around the globe. Wearing a mask and social distancing have become a new culture to limit the transmission of this deadly virus. While we hope to return back to our normal life from few years back, vaccination is the key, not only in one county or region but through out the entire world. Therefore it is necessary to track the vaccination progress of every country to save lives, limit spread, and move back to our old normal. In this project, I will track the vaccination progress around the globe based on the vaccine they use, total vaccinations, and daily vaccinations rate.

# ### Understanding Dataset

# The vaccination progress dataset is obtained from Kaggle. The data contains the following information:
# 
# 1. Country- this is the country for which the vaccination information is provided;
# 2. Country ISO Code - ISO code for the country;
# 3. Date - date for the data entry; for some of the dates we have only the daily vaccinations, for others, only the (cumulative) total;
# 4. Total number of vaccinations - this is the absolute number of total immunizations in the country;
# 5. Total number of people vaccinated - a person, depending on the immunization scheme, will receive one or more (typically 2) vaccines; at a certain moment, the number of vaccination might be larger than the number of people;
# 6. Total number of people fully vaccinated - this is the number of people that received the entire set of immunization according to the immunization scheme (typically 2); at a certain moment in time, there might be a certain number of people that received one vaccine and another number (smaller) of people that received all vaccines in the scheme;
# 7. Daily vaccinations (raw) - for a certain data entry, the number of vaccination for that date/country;
# 8. Daily vaccinations - for a certain data entry, the number of vaccination for that date/country;
# 9. Total vaccinations per hundred - ratio (in percent) between vaccination number and total population up to the date in the country;
# 10. Total number of people vaccinated per hundred - ratio (in percent) between population immunized and total population up to the date in the country;
# 11. Total number of people fully vaccinated per hundred - ratio (in percent) between population fully immunized and total population up to the date in the country;
# 12. Number of vaccinations per day - number of daily vaccination for that day and country;
# 13. Daily vaccinations per million - ratio (in ppm) between vaccination number and total population for the current date in the country;
# 14. Vaccines used in the country - total number of vaccines used in the country (up to date);
# 15. Source name - source of the information (national authority, international organization, local organization etc.);
# 16. Source website - website of the source of information
# 
# <u><b>Acknowledgement:</u></b><br>
#     The data is made available in Kaggle by [Gabriel Preda](https://www.kaggle.com/gpreda). The dataset information provided above is as mentioned by the author.

# ### Libraries
# 

# In[33]:


#dataframe
import pandas as pd
import numpy as np

#visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import cufflinks as cf
import chart_studio.plotly as py

get_ipython().run_line_magic('matplotlib', 'inline')

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
cf.go_offline()


# suppressing warnings
import warnings
warnings.filterwarnings('ignore')


# ### Importing Dataset

# In[2]:


df = pd.read_csv("/Users/bs/Mac Drive/Dev/COVID Vaccination/country_vaccinations.csv")
df.head()


# ### Exploratory Data Analysis

# In[3]:


#Dataframe column characteristics
df.info()


# In[4]:


#rows and columns in the dataframe
df.shape


# In[5]:


#number of empty cells in the data frame
df.isnull().sum()


# In[6]:


#list of different names of countries in the dataset
df["country"].unique()


# In[7]:


#list of vaccines names
df['vaccines'].unique()


# In[8]:


#total number of countries
len(df['country'].unique())


# In[9]:


# total number of vaccines/vaccine combinations
len(df['vaccines'].unique())


# ### Data Visualization

# In[10]:


#Daily vaccination rate in the US
px.line(df[df['country']=='United States'],x='date',y='daily_vaccinations').update_layout(title = 'Daily Vaccination Rate in the US',xaxis_title='Date',yaxis_title='Daily Vaccination' )


# In[11]:


#Daily Vaccination rate in the UK
fig=go.Figure()
df1=df[df['country']=='United Kingdom']
fig.add_trace(go.Scatter(x=df1.date,y=df1.daily_vaccinations,mode='lines+markers',name='UK'))
fig.update_layout(title = 'Daily Vaccination Rate in the UK',xaxis_title='Date',yaxis_title='Daily Vaccination' )


# In[12]:


#Daily Vaccination Rate in Canada
px.line(df[df['country']=='Canada'],x='date',y='daily_vaccinations').update_layout(title = 'Daily Vaccination Rate in Canda',xaxis_title='Date',yaxis_title='Daily Vaccination' )


# In[13]:


#Daily Vaccination Rate Comparision
fig=go.Figure()
df1=df[df['country']=='United States']
df2=df[df['country']=='United Kingdom']
df3=df[df['country']=='Canada']
fig.add_trace(go.Scatter(x=df1.date,y=df1.daily_vaccinations,mode='lines+markers',name='US'))
fig.add_trace(go.Scatter(x=df2.date,y=df2.daily_vaccinations,mode='lines+markers',line=dict(color='firebrick',width=2),name='UK'))
fig.add_trace(go.Scatter(x=df3.date,y=df3.daily_vaccinations,mode='lines+markers',line=dict(dash='dashdot'),name='Canada'))

fig.update_layout(title = 'Daily Vaccination Rate Comparision in the US, UK & Canada',xaxis_title='Date',yaxis_title='Daily Vaccination' )


# In[14]:


#Number of counties using different vaccine types/combinations
df.groupby(['country'],sort=False, as_index=False)['vaccines'].first()
plt.figure(figsize=(15,5))
plt.xticks(rotation=90)
sns.set(style = 'whitegrid')
sns.countplot(x="vaccines", data=df.groupby(['country'],sort=False, as_index=False)['vaccines'].first())
plt.title("Countries using Different Vaccines Types\n",size =20)
plt.ylabel("No of Countries",size=15)
plt.xlabel("\nVaccine Types\n\n",size=15)


# In[15]:


#Finding Maximum number of people vaccinated in each country
vaccine = df.groupby(["country","vaccines"])['total_vaccinations','total_vaccinations_per_hundred',
                                       'daily_vaccinations','daily_vaccinations_per_million'].max().reset_index()
vaccine


# In[16]:


#Map showing vaccine types and total vaccination
fig=px.scatter_geo(vaccine, locations='country',locationmode='country names',color='vaccines', size='total_vaccinations',hover_name='vaccines', projection='natural earth')
fig.update_layout(title='Vaccine Used by Countries with Total Vaccinated', legend_orientation='h',legend_title_text='Vaccine')


# In[17]:


#Visualization using choropleth
fig=px.choropleth(vaccine, locations='country',locationmode = 'country names', color='vaccines')
fig.update_layout(title='Color representation of Vaccine Used', legend_orientation='h', legend_title_text='Vaccine')


# In[18]:


#Showing Total Vaccinated in TreeMap
fig=px.treemap(vaccine,path=['vaccines','country'],values='total_vaccinations')
fig.update_layout(title='Tree Map based on Total Vaccination')
fig


# In[19]:


#Showing Daily Vaccinated in TreeMap
fig=px.treemap(vaccine,path=['vaccines','country'],values='daily_vaccinations')
fig.update_layout(title='Tree Map based on Daily Vaccination Rate')
fig


# In[20]:


#Map based on Total Vaccination
fig=px.choropleth(vaccine, locations='country', locationmode='country names', color='total_vaccinations')
fig.update_layout(title='Total Vaccinations by Country')
fig


# In[21]:


#Map based on Daily Vaccination
fig=px.choropleth(vaccine, locations='country', locationmode='country names', color='daily_vaccinations')
fig.update_layout(title='Daily Vaccinations by Country')
fig


# In[22]:


#Map based on vaccination per hundred
fig=px.choropleth(vaccine, locations='country', locationmode='country names', color='total_vaccinations_per_hundred')
fig.update_layout(title='Total Vaccinations Per Hundred by Country')
fig


# In[23]:


#Countries with low total vaccination rate
adf=vaccine.sort_values(by='total_vaccinations').head(9)
adf


# In[24]:


#Bargraph showing low total vaccinated counties
fig= px.bar(adf, x= 'country', y ='total_vaccinations',color='vaccines')
fig.update_layout(title='Countries with Low Total Vaccination and Vaccine Used')
fig


# In[25]:


#Countries with high total vaccination rate
adf=vaccine.sort_values(by='total_vaccinations',ascending=False).head(9)
adf


# In[26]:


#Bargraph showing high total vaccinated counties
fig= px.bar(adf, x= 'country', y ='total_vaccinations',color='vaccines')
fig.update_layout(title='Countries with High Total Vaccination and Vaccine Used')
fig


# In[27]:


#Countries with low daily vaccination rate
adf=vaccine.sort_values(by='daily_vaccinations').head(9)
adf


# In[28]:


#Bargraph showing low daily vaccinated counties
fig= px.bar(adf, x= 'country', y ='daily_vaccinations',color='vaccines')
fig.update_layout(title='Countries with Low daily Vaccination and Vaccine Used')
fig


# In[29]:


#Countries with high daily vaccination rate
adf=vaccine.sort_values(by='daily_vaccinations',ascending=False).head(9)
adf


# In[30]:


#Bargraph showing high daily vaccinated counties
fig= px.bar(adf, x= 'country', y ='daily_vaccinations',color='vaccines')
fig.update_layout(title='Countries with High daily Vaccination and Vaccine Used')
fig


# In[31]:


#Total of each Vaccine used
vac = df.groupby("vaccines")['total_vaccinations'].sum().astype(int).reset_index()
vac


# In[32]:


#Piechart showing total different combinations of vaccines used by countries
fig=px.pie(vac,values='total_vaccinations',names='vaccines',labels={'vaccines':'Vaccine','total_vaccinations':'Total'})
fig.update_layout(title='Total vaccines given by Vaccines/Vaccines combinations')
fig


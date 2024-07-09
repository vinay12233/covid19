import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import random
from PIL import Image
logo = Image.open('logo.png')
#pip install pandas numpy matplotlib seaborn streamlit
#to run streamlit :   streamlit run netflix.py 
st.set_page_config(page_title="COVID-19  EDA", page_icon=":bar_chart:", layout="wide")
st.image(logo)
# Define the list of names
names = ["21A21A6111-E Jeji Anil", "21A21A6123-K Vamsi"]
st.title("Exploratory Data Analysis on COVID-19 Data Set")
# Add the names to the sidebar
st.sidebar.title("Project Team Members:")

for name in names:
    st.sidebar.write(name)
st.sidebar.title("Under The Guidance of :")
st.sidebar.write("Dr.Bomma.Ramakrishna")
# File upload
uploaded_file = st.file_uploader("Choose a COVID-19 Dataset csv")
if uploaded_file is not None:
    data=pd.read_csv(uploaded_file)
    st.dataframe(data)

    st.title("COVID-19 Data Analysis")

    # Checkboxes for questions
    
    # Question 1
    
    if st.checkbox("Q1: Show the number of Confirmed, Deaths, and Recovered cases in each Region"):
           st.write(data.groupby('Region')[['Confirmed', 'Deaths', 'Recovered']].sum())
    # Question 2
    
    if st.checkbox("Q2: Remove all the records where Confirmed Cases is Less Than 10"):
          data = data[~(data.Confirmed < 10)]
          st.write(data)
            
    # Question 3
    
    if st.checkbox("Q3: In which Region, maximum number of Deaths cases were recorded?"):
           st.write(data.groupby('Region')['Confirmed'].sum().sort_values(ascending=False).head(1))
        
    # Question 4
    
    if st.checkbox("Q4: In which Region, minimum number of Deaths cases were recorded?"):
           st.write(data.groupby('Region')['Deaths'].sum().sort_values().head(1))
        
    # Question 5
    
    if st.checkbox("Q5: How many Confirmed, Deaths & Recovered cases were reported from India till 29 April 2020?"):
           india_data = data[data['Region'] == 'India']
           st.write("Confirmed cases:", india_data['Confirmed'].sum())
           st.write("Deaths:", india_data['Deaths'].sum())
           st.write("Recovered:", india_data['Recovered'].sum())
            
    # Question 6-A
    
    if st.checkbox("Q6-A: Sort the entire data wrt No. of Confirmed cases in ascending order"):
           st.write(data.sort_values(by=['Confirmed'], ascending=True))
        
     # Question 6-B  
    
    if st.checkbox("Q6-B: Sort the entire data wrt No. of Recovered cases in descending order"):
           st.write(data.sort_values(by=['Recovered'], ascending=False))


    # Question 7

    if st.checkbox("Q7: Check if the patient is likely to have COVID-19 based on symptoms"):
          # Create checkboxes for symptoms
          fever = st.checkbox("Fever")
          cough = st.checkbox("Dry Cough")
          tiredness = st.checkbox("Tiredness")
          breathing_difficulty = st.checkbox("Difficulty in Breathing")
          sore_throat = st.checkbox("Sore Throat")
          body_aches = st.checkbox("Body Aches")
          loss_of_smell_or_taste = st.checkbox("Loss of Smell or Taste")

    # Check if any of the symptoms are present
          if fever or cough or tiredness or breathing_difficulty or sore_throat or body_aches or loss_of_smell_or_taste:
                st.write("Based on the symptoms, the patient may have COVID-19.")
          else:
                st.write("Based on the symptoms, the patient is unlikely to have COVID-19.")

    # Question 8
    if st.checkbox("Q8: Which Region has the highest number of Confirmed cases?"):
           st.write(data.groupby('Region')['Confirmed'].sum().sort_values(ascending=False).head(1).index[0])

    
        
    # Question 9  
    
    if st.checkbox("Q9: Which region have a death rate of over 10%?"):
           data['Death Rate'] = (data['Deaths'] / data['Confirmed']) * 100
           high_death_rate = data[data['Death Rate'] > 10]['Region']
           st.write(high_death_rate.unique()) 
           
    # Question 10  
           
    if st.checkbox("Q10: Which region have the highest mortality rates (number of deaths / number of confirmed cases)?"):
           #Calculate mortality rate
           data['Mortality_Rate'] = data['Deaths'] / data['Confirmed']
           #Group data by country and sort by mortality rate
           mortality_by_Region = data.groupby('Region')['Mortality_Rate'].max().sort_values(ascending=False)
           st.write(mortality_by_Region)
    
    # Question 11
    if st.checkbox("Q11: Show a line graph showing the total confirmed cases for each region (top 8)"):
           region_confirmed = data.groupby("Region")["Confirmed"].sum().reset_index()
           region_confirmed = region_confirmed.sort_values("Confirmed", ascending=False).head(8)
           fig, ax = plt.subplots()
           sns.lineplot(x="Region", y="Confirmed", data=region_confirmed, ax=ax)
           ax.set_title("Total Confirmed Cases by Region (Top 8)")
           ax.set_xlabel("Region")
           ax.set_ylabel("Confirmed Cases")
           st.pyplot(fig)
    
    # Question 12
    if st.checkbox("Q12: Create a histogram showing the distribution of Confirmed, Deaths, and Recovered cases over time."):
          data_by_date = data.groupby(['Date'])[['Confirmed', 'Deaths', 'Recovered']].sum()
          data_by_date.hist(bins=10, figsize=(12,8))
          plt.xlabel('Number of Cases')
          plt.ylabel('Frequency')
          plt.title('Distribution of COVID-19 Cases Over Time')
          st.pyplot()
    
    
    
    
    
    # Question 13
    st.set_option('deprecation.showPyplotGlobalUse', False)
    if st.checkbox("Q13: Show a bar chart of the top 10 Regoins with the highest number of confirmed cases."):
           top10 = data.groupby('Region')['Confirmed'].sum().sort_values(ascending=False).head(10)
           plt.figure(figsize=(12,6))
           plt.title("Top 10 Regions with Highest Number of Confirmed Cases", fontsize=18)
           plt.xlabel("Region", fontsize=14)
           plt.ylabel("Number of Confirmed Cases", fontsize=14)
           sns.barplot(x=top10.index, y=top10.values)
           st.pyplot()
        
    # Question 14

    if st.checkbox("Q14: Show the trend of Confirmed, Deaths, and Recovered cases over time for a selected region"):
           # Create a dropdown menu for region selection
           regions = data['Region'].unique()
           selected_region = st.selectbox("Select a region", regions)

           # Filter data for the selected region
           region_data = data[data['Region'] == selected_region]

           # Scatter plot showing the trend of Confirmed, Deaths, and Recovered cases over time
           fig, ax = plt.subplots(figsize=(12, 8))
           ax.scatter(region_data['Date'], region_data['Confirmed'], label='Confirmed')
           ax.scatter(region_data['Date'], region_data['Deaths'], label='Deaths')
           ax.scatter(region_data['Date'], region_data['Recovered'], label='Recovered')
           ax.set_xlabel('Date')
           ax.set_ylabel('Number of Cases')
           ax.set_title(f"{selected_region} COVID-19 Cases")
           ax.legend()
           st.pyplot(fig)






    # Question 15
    if st.checkbox("Q15: What is the distribution of Confirmed cases?"):
           # Create a histogram of confirmed cases
           fig, ax = plt.subplots()
           ax = sns.histplot(data=data, x='Confirmed', kde=True)
           ax.set_title('Distribution of Confirmed Cases')
           st.pyplot(fig)
            
    # Question 16

    if st.checkbox("Q16: Show a pie chart representing the number of confirmed, deaths, and recovered cases for each country"):
           # Group data by country and sum the cases
           grouped_data = data.groupby('Region')[['Confirmed', 'Deaths', 'Recovered']].sum()
    
           # Create a new figure and subplot
           fig, ax = plt.subplots(figsize=(10, 10))
    
           # Plot the data as a pie chart
           ax.pie(grouped_data.sum(), labels=grouped_data.columns, autopct='%1.1f%%', startangle=90)
           ax.axis('equal')
           ax.set_title('COVID-19 Cases By Region')
    
           # Show the plot
           st.pyplot(fig)
        
    # Question 17
    if st.checkbox("Q17: What is the average number of confirmed cases per day globally?"):
        average_daily_cases = data.groupby('Date')['Confirmed'].sum().mean()
        st.write(f"Average daily confirmed cases globally: {average_daily_cases:.2f}")

    # Question 18
    if st.checkbox("Q18: Show the top 10 regions with the highest number of recovered cases."):
        top_regions_recovered = data.groupby('Region')['Recovered'].sum().nlargest(10)
        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_regions_recovered.index, y=top_regions_recovered.values)
        plt.title('Top 10 Regions with Highest Number of Recovered Cases')
        plt.xlabel('Region')
        plt.ylabel('Number of Recovered Cases')
        st.pyplot()

   

    # Question 19
    if st.checkbox("Q19: Compare the mortality rates (deaths/confirmed) between two selected regions."):
        regions = data['Region'].unique()
        region1 = st.selectbox("Select the first region", regions)
        region2 = st.selectbox("Select the second region", regions)
        mortality_rate_region1 = data[data['Region'] == region1]['Deaths'].sum() / data[data['Region'] == region1]['Confirmed'].sum()
        mortality_rate_region2 = data[data['Region'] == region2]['Deaths'].sum() / data[data['Region'] == region2]['Confirmed'].sum()
        st.write(f"Mortality rate in {region1}: {mortality_rate_region1:.4f}")
        st.write(f"Mortality rate in {region2}: {mortality_rate_region2:.4f}")

    


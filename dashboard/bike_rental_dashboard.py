import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load the dataset
all_data = pd.read_csv("Bike-Rental-Analysis/dashboard/main_data.csv")

# Convert date columns to datetime
all_data["dteday"] = pd.to_datetime(all_data["dteday"])
all_data["hr"] = pd.to_datetime(all_data["hr"], format="%H").dt.hour

# Filter and clean data
def filter_data(start_date, end_date):
    # Convert start_date and end_date to datetime64[ns]
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Filter the data
    filtered_data = all_data[(all_data["dteday"] >= start_date) & (all_data["dteday"] <= end_date)]
    
    return filtered_data

# Generate a function for boxplot to show the effect of weather on rentals
def plot_weather_effect(filtered_data):
    fig, ax = plt.subplots(1, 2, figsize=(20, 6))

    # Casual users
    sns.boxplot(x='weathersit', y='casual', data=filtered_data, ax=ax[0])
    ax[0].set_title('Weather Effect on Casual Rentals')
    ax[0].set_xlabel('Weather Situation')
    ax[0].set_ylabel('Casual Rentals')

    # Registered users
    sns.boxplot(x='weathersit', y='registered', data=filtered_data, ax=ax[1])
    ax[1].set_title('Weather Effect on Registered Rentals')
    ax[1].set_xlabel('Weather Situation')
    ax[1].set_ylabel('Registered Rentals')

    st.pyplot(fig)

# Generate a function for line plot for the effect of day of the week
def plot_day_effect(filtered_data):
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.lineplot(x='weekday', y='casual', data=filtered_data, label='Casual Rentals', ax=ax)
    sns.lineplot(x='weekday', y='registered', data=filtered_data, label='Registered Rentals', ax=ax)
    
    ax.set_title('Day of the Week Effect on Rentals')
    ax.set_xlabel('Day of Week (0=Sunday, 6=Saturday)')
    ax.set_ylabel('Number of Rentals')
    ax.legend()

    st.pyplot(fig)

# Generate a function for the effect of temperature and season
def plot_season_and_temp_effect(filtered_data):
    fig, ax = plt.subplots(1, 2, figsize=(20, 6))

    # Temperature effect
    sns.scatterplot(x='temp', y='casual', data=filtered_data, label='Casual Rentals', ax=ax[0])
    sns.scatterplot(x='temp', y='registered', data=filtered_data, label='Registered Rentals', ax=ax[0])
    ax[0].set_title('Temperature Effect on Rentals')
    ax[0].set_xlabel('Temperature')
    ax[0].set_ylabel('Number of Rentals')
    ax[0].legend()

    # Season effect
    sns.barplot(x='season', y='casual', data=filtered_data, ax=ax[1])
    sns.barplot(x='season', y='registered', data=filtered_data, ax=ax[1])
    ax[1].set_title('Season Effect on Rentals')
    ax[1].set_xlabel('Season')
    ax[1].set_ylabel('Number of Rentals')
    ax[1].legend()

    st.pyplot(fig)

# Streamlit App Layout
st.title('Bike Rentals Analysis Dashboard')

# Sidebar for date range selection
with st.sidebar:
    st.image("analis_image.png")  
    st.header('Select Date Range')
    start_date = st.date_input('Start Date', all_data["dteday"].min())
    end_date = st.date_input('End Date', all_data["dteday"].max())

# Filter the data based on selected date range
filtered_data = filter_data(start_date, end_date)

# Calculate total casual, registered, and overall rentals
total_casual = filtered_data['casual'].sum()
total_registered = filtered_data['registered'].sum()
total_rentals = filtered_data['cnt'].sum()

# Display the key metrics at the top of the page
st.header("Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Casual Rentals", value=total_casual)

with col2:
    st.metric(label="Total Registered Rentals", value=total_registered)

with col3:
    st.metric(label="Overall Total Rentals", value=total_rentals)

# Display weather effects on rentals
st.header('Weather Effect on Rentals')
plot_weather_effect(filtered_data)

# Display day of the week effect
st.header('Day of the Week Effect on Rentals')
plot_day_effect(filtered_data)

# Display temperature and season effects
st.header('Temperature and Season Effect on Rentals')
plot_season_and_temp_effect(filtered_data)

st.caption('Bike Rentals Analysis Dashboard - Made by Muhammad Fikri Abdullah')

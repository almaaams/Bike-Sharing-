import pandas as pd
import plotly.express as px
import streamlit as st

# Load data
day_df = pd.read_csv("https://raw.githubusercontent.com/almaaams/project_akhir/main/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/almaaams/project_akhir/main/hour.csv")

# Prepare data for temperature analysis
day_df['temp_celsius'] = day_df['temp'] * 41 - 8
day_df['temp_category'] = pd.cut(day_df['temp_celsius'], 
                                 bins=[-10, 0, 10, 20, 30, 40], 
                                 labels=['Very Cold', 'Cold', 'Mild', 'Warm', 'Hot'])

# Prepare data for hourly analysis
hourly_rentals = hour_df.groupby(['hr', 'workingday'])['cnt'].mean().unstack()

# Function to create temperature rentals chart
def create_temp_rentals_chart():
    temp_category_means = day_df.groupby('temp_category')[['casual', 'registered', 'cnt']].mean().reset_index()
    fig = px.bar(temp_category_means, x='temp_category', y=['casual', 'registered', 'cnt'],
                 title='Average Bike Rentals by Temperature Category',
                 labels={'value': 'Average Rentals', 'temp_category': 'Temperature Category', 'variable': 'User Type'},
                 barmode='group')
    return fig

# Function to create hourly rentals chart
def create_hourly_rentals_chart():
    fig = px.line(hourly_rentals, title='Bike Rental Patterns by Hour',
                  labels={'value': 'Average Rentals', 'hr': 'Hour'})
    fig.update_layout(legend_title_text='Day Type', xaxis_title='Hour')
    return fig

# Set up Streamlit dashboard layout
st.title('Bike Rental Analysis Dashboard')

# Display temperature rentals chart
st.subheader('Temperature vs Bike Rentals')
st.plotly_chart(create_temp_rentals_chart(), use_container_width=True)

# Display hourly rentals chart
st.subheader('Hourly Bike Rentals Pattern')
st.plotly_chart(create_hourly_rentals_chart(), use_container_width=True)

# Display key statistics
st.subheader('Rental Statistics')

# Calculate statistics
correlation = day_df['temp_celsius'].corr(day_df['cnt'])
peak_hour_workday = hourly_rentals[1].idxmax()
peak_hour_weekend = hourly_rentals[0].idxmax()

# Display statistics in a table
st.table(pd.DataFrame({
    'Metric': ['Temperature-Total Rentals Correlation', 'Peak Hour (Workday)', 'Peak Hour (Weekend)'],
    'Value': [f"{correlation:.2f}", peak_hour_workday, peak_hour_weekend]
}))

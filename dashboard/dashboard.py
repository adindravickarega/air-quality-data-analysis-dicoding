import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Load your combined DataFrame
@st.cache
def load_data():
    # Assuming 'combined_df' is saved as a CSV file after your data cleaning and wrangling steps
    return pd.read_csv('main_data.csv')

combined_df = load_data()

# Sidebar for navigation
st.sidebar.title("Air Quality Data Analysis")
page = st.sidebar.selectbox("Select a page", ["Home", "PM2.5 Trends", "Correlations"])

if page == "Home":
    st.title("Air Quality Data Analysis in China (2013-2017)")
    st.write("This dashboard presents the analysis of air quality data, focusing on PM2.5 levels.")
    st.write("Use the sidebar to navigate through different analyses.")

elif page == "PM2.5 Trends":
    st.title("PM2.5 Trends (2013 - 2017) by Station")
    
    # Group the data for PM2.5 trends
    pm25_trends = combined_df.groupby(['year', 'station'])['pm2.5'].mean().reset_index()

    # Plotting PM2.5 trends
    fig = px.line(pm25_trends, x='year', y='pm2.5', color='station',
                  markers=True, 
                  title='PM2.5 Trends (2013 - 2017) by Station',
                  labels={'pm2.5': 'Average PM2.5 Level', 'year': 'Year'},
                  hover_data={'year': True, 'pm2.5': True, 'station': True})
    
    st.plotly_chart(fig)

    # Stacked bar chart
    average_pm25 = combined_df.groupby(['station', 'year'])['pm2.5'].mean().reset_index()
    fig2 = go.Figure()

    for year in average_pm25['year'].unique():
        year_data = average_pm25[average_pm25['year'] == year]
        fig2.add_trace(go.Bar(
            x=year_data['station'],
            y=year_data['pm2.5'],
            name=str(year),
            hoverinfo='x+y'
        ))

    fig2.update_layout(
        title='Average PM2.5 Values by Station (2013 - 2017)',
        barmode='stack',
        xaxis_title='Station',
        yaxis_title='Average PM2.5 Level',
    )

    st.plotly_chart(fig2)

elif page == "Correlations":
    st.title("Correlation Analysis")
    
    # Correlation heatmap
    correlation_columns = ['pm2.5', 'pm10', 'so2', 'no2', 'co', 'o3', 'temp', 'pres', 'dewp', 'rain', 'wspm']
    correlation_matrix = combined_df[correlation_columns].corr()

    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
    plt.title('Correlation Heatmap of Weather Factors and Pollutants', fontsize=16)
    st.pyplot(plt)

    st.write("From the heatmap, you can observe the correlations between different pollutants and weather factors.")

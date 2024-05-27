import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Investigating how parameters affect the sale price for vehicles sold in the US between May 2018 and April 2019')

df = pd.read_csv('vehicles_us.csv')

# Days listed vs price
days_price = px.scatter(df, x='days_listed', y='price', title='Days listed vs price of vehicle', labels={'x': 'days listed', 'y': 'Price $'}, opacity=0.7)
# Plot scatter plot for days listed vs price
# Remove outliers
days_price_df = df[df['price']<100000]
days_price_df = days_price_df[days_price_df['days_listed']<200]
days_price = px.scatter(days_price_df, x='days_listed', y='price', title='Days listed vs price of vehicle', labels={'x': 'days listed', 'y': 'Price $'}, opacity=0.7)

# Plot price vs odometer
# remove rows where odometer is NaN
odo_df = df.dropna(subset=['odometer'])
# Remove outliers for odometer above 400,000
odo_df = odo_df[odo_df['odometer']<400000]
# Remove outliers for price over $60k
odo_df = odo_df[odo_df['price']<60000]
odo_df.info()
odo_plot = px.scatter(odo_df, x='odometer', y='price', title='Odometer vs price of vehicle', labels={'x': 'Odometer', 'y': 'Price $'}, opacity=0.7)

# Explore relationship between condition and days listed
days_to_sell_condition = df.groupby('condition')['days_listed'].mean().round(1)
days_to_sell_condition = pd.DataFrame(days_to_sell_condition).reset_index()
Colors = ['red', 'blue', 'green', 'yellow', 'pink', 'purple']
dc_bar = px.bar(days_to_sell_condition, x='condition', y='days_listed', color=Colors, title='How many days to sell based on car condition')
dc_bar.update_layout(yaxis=dict(range=[30, 40]))

# Explore df based on price and type of vehicle
# Remove outliers based on price
price_typeh = df[df['price']<50000]
# Histogram for price and type of vehicles
pt_hist = px.histogram(price_typeh, x='price', color = 'type', title='Price of vehicle based on type', nbins=50, opacity=0.7)

# Explore df based on price and condition of vehicle
# Remove outliers based on price
pc = df[df['price']<50000]
# Histogram for price and type of vehicles
pc_hist = px.histogram(pc, x='price', color = 'condition', title='Price of vehicle based on condition', nbins=50, opacity=0.7)

# Checkboxes
st.header('Select one or more of the following parameters to see how it affects vehicle price:')
check = st.checkbox('Days Listed')
check1 = st.checkbox('Miles on Odometer')
check2 = st.checkbox('Car Condition')
check3 = st.checkbox('Car Type')

if check:
    st.write(days_price)
    st.write(dc_bar)
    st.write('Vehicles listed as "new" sold 2 days sooner on average.')

if check1:
    st.write(odo_plot)
    st.write('There is an inverse relationship between sale price and miles on the odometer.')

if check2:
    st.write(pc_hist)
    st.write(dc_bar)
    st.write('Vehicles listed as "new" sold 2 days sooner on average.')
    st.write('Almost half of the vehicles (48%) were listed in "excellent" condition.')

if check3:
    st.write(pt_hist)

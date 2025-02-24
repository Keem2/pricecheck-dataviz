import streamlit as st
import pandas as pd 
import math

df = pd.read_csv('../prices_file.csv')
df_clean = df.dropna(how="all")

def find_average(df, column='price'):
    if column not in df.columns:
        return 0  # Return 0 if the column doesn't exist
    else:
        return df[column].dropna().mean()  # Drop NaN values and calculate mean

# Category dropdown values
categories = df_clean['category'].drop_duplicates().sort_values().to_list()

st.title("Pricecheck BB Dashboard :flag-bb:")

# category select dropdown
category_option = st.selectbox("Select a category",categories)

# filtering dataframe to make a new dataframe where the rows in it are only equals to category_option
filtered_df_for_subcat = df[df['category'] == category_option]

# Subategory dropdown values
subcategories = filtered_df_for_subcat['subcategory'].drop_duplicates().sort_values().to_list()

subcategory_option = st.selectbox("Select a subcategory",subcategories)

# filtering dataframe to make a new dataframe where the rows in it are only equals to subcategory_option
filtered_df_for_products = df[df['subcategory'] == subcategory_option]

# Product dropdown values
products = filtered_df_for_products['product_name'].drop_duplicates().sort_values().to_list()

selected_product = st.selectbox("Select a product",products)

# filtering dataframe to make a new dataframe where the rows in it are only equals to selected_product
product_info_df = df[df['product_name'] == selected_product]

# accessing row which has the lowest price, and converting it to a dict
lowest_price_row = df.loc[product_info_df['price'].dropna().idxmin()].to_dict()

# lowest price ever vendor
lowest_price_vendor = lowest_price_row['vendor_group_name']

# lowest ever price
lowest_price = lowest_price_row['price']

# average price
avg = product_info_df["price"].dropna().mean()

# product info from most recent reference date
recent_product_info_ = product_info_df[product_info_df['reference_date'] == product_info_df['reference_date'].max()]
recent_product_info_df = recent_product_info_[['vendor_group_name','price']]

  

with st.container(border=True):
    st.subheader("Lowest Price Recorded")
    st.metric(value=lowest_price, label_visibility='collapsed', label="Lowest Price Recorded")
    st.text(f"Found at {lowest_price_vendor}")

with st.container(border=True):
    st.subheader("Average Price")
    st.metric(value=avg, label_visibility='collapsed', label="Average Price")

dates = product_info_df['reference_date'].drop_duplicates().sort_values().to_list()

# lowest price for each date
df_min_prices = product_info_df.groupby('reference_date')['price'].min().reset_index()


price_chart_data = pd.DataFrame(
    {
        "Reference Date": df_min_prices['reference_date'].to_list(),
         "Price": df_min_prices['price'].to_list(),
    
        
        
    }
)
st.header("Lowest Price History", divider="gray")
st.line_chart(price_chart_data, x="Reference Date",y="Price")
    
    


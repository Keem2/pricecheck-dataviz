import streamlit as st
import pandas as pd

df = pd.read_csv('prices_file.csv')
df_clean = df.dropna(how="all")

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
lowest_price_ever_vendor = lowest_price_row['vendor_group_name']

# lowest ever price
lowest_price_ever = lowest_price_row['price']

#lowest ever price date
lowest_price_ever_date = lowest_price_row['reference_date']

# average price
avg = product_info_df["price"].dropna().mean()

# product info from most recent reference date
recent_product_info_df = product_info_df[product_info_df['reference_date'] == product_info_df['reference_date'].max()].sort_values("price",ascending=True)

# current lowest price of product
lowest_current_price = recent_product_info_df['price'].min()

#list of vendors with lowest price from most recent reference date
lowest_price_vendor_list = recent_product_info_df[recent_product_info_df['price'] == lowest_current_price]['vendor_group_name'].to_list()

# table data
price_table_data = pd.DataFrame(
    {
        "Vendor": recent_product_info_df['vendor_group_name'],
        "Price": recent_product_info_df['price'].apply(
    lambda x: '${:,.2f}'.format(x) if pd.notna(x) else None
)
    }
)


st.subheader("Current Prices")
st.text(f"Last updated: {recent_product_info_df['reference_date'].max()}")
st.dataframe(price_table_data,hide_index=True, use_container_width=True)

# bar chart data
price_bar_chart_data = pd.DataFrame(
    {
        "Vendor": recent_product_info_df['vendor_group_name'],
        "Price": recent_product_info_df['price']
    }
)
st.bar_chart(price_bar_chart_data,x="Vendor",y="Price")
  
# formatting list of lowest_price_vendor_list into a string
vendor_list_string = ''
last_item = lowest_price_vendor_list[-1]
for vendor in lowest_price_vendor_list:
    if len(lowest_price_vendor_list) == 1:
        vendor_list_string+=vendor
    elif vendor == last_item:
        vendor_list_string+=vendor
    else:
        vendor_list_string+=vendor+", "
        
with st.container(border=True):
    st.subheader("Lowest Price Now")
    current_lowest_price_string = '${:,.2f}'.format(lowest_current_price)
    st.metric(value=current_lowest_price_string, label_visibility='collapsed', label="Current Lowest Price")
    st.text(f"Found at {vendor_list_string}")

with st.container(border=True):
    st.subheader("Lowest Price Recorded")
    lowest_price_ever_string = '${:,.2f}'.format(lowest_price_ever)
    st.metric(value=lowest_price_ever_string, label_visibility='collapsed', label="Lowest Price Recorded")
    st.text(lowest_price_ever_date)
    st.text(lowest_price_ever_vendor)

with st.container(border=True):
    st.subheader("Average Price")
    avg_price_string = '${:,.2f}'.format(avg)
    st.metric(value=avg_price_string, label_visibility='collapsed', label="Average Price")

dates = product_info_df['reference_date'].drop_duplicates().sort_values().to_list()

# lowest price for each date
df_min_prices = product_info_df.groupby('reference_date')['price'].min().reset_index() 

# line chart data
price_line_chart_data = pd.DataFrame(
    {
        "Reference Date": df_min_prices['reference_date'].to_list(),
        "Price": df_min_prices['price'].to_list(),
    }
)
st.header("Lowest Price History", divider="gray")
st.line_chart(price_line_chart_data, x="Reference Date",y="Price")
    
    


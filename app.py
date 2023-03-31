import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Pizza sales analysis',
                   page_icon=":pizza:",
                   layout="wide",
                   initial_sidebar_state='auto')

@st.cache_data
def get_data():
    dataframe = pd.read_excel("Data Model - Pizza Sales.xlsx")
    dataframe['hour'] = pd.to_datetime(dataframe['order_time'], format='%H:%M:%S').dt.hour
    return dataframe


df = get_data()


st.sidebar.header('Filter here:')
category = st.sidebar.multiselect(
    "Select the pizza category:",
    options=df['pizza_category'].unique(),
    default=df['pizza_category'].unique()
)

size = st.sidebar.multiselect(
    "Select the pizza size:",
    options=df['pizza_size'].unique(),
    default=df['pizza_size'].unique()
)

df_selection = df.query(
    "pizza_category == @category & pizza_size == @size"
)


st.title(":bar_chart: Pizza sales Dashboard")
st.markdown("##")

total_sales = int(df_selection['total_price'].sum())
total_quantity = int(df_selection['quantity'].sum())
average_sale_by_transaction = round(df_selection['total_price'].mean(), 2)

left, middle, right = st.columns(3)

with left:
    st.subheader('Total Pizza sales:')
    st.subheader(f"${total_sales:,}")

with middle:
    st.subheader('Total quantity sold:')
    st.subheader(f"${total_quantity}")

with right:
    st.subheader('Average sales per transaction:')
    st.subheader(f"${average_sale_by_transaction}")

st.markdown("---")

sales_by_category = (
    df_selection.groupby(by=['pizza_category']).sum()[['total_price']].sort_values(by='total_price')
)

fig_product_sales = px.bar(
    sales_by_category,
    x='total_price',
    y=sales_by_category.index,
    orientation='h',
    title="<b>Sales by pizza category</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_category),
    template="plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False))
)


sales_by_hour = df_selection.groupby(by=['hour']).sum()[['total_price']]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y='total_price',
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template='plotly_white'
)

fig_hourly_sales.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(tickmode='linear'),
    yaxis=(dict(showgrid=False))
)


left_col, right_col = st.columns(2)
left_col.plotly_chart(fig_hourly_sales, use_container_width=True)
right_col.plotly_chart(fig_product_sales, use_container_width=True)

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """

st.markdown(hide_st_style, unsafe_allow_html=True)
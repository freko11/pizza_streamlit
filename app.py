import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Pizza sales analysis',
                   page_icon=":pizza:",
                   layout="wide",
                   initial_sidebar_state='auto')

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """

st.markdown(hide_st_style, unsafe_allow_html=True)

@st.cache_data
def get_data():
    df = pd.read_excel("Data Model - Pizza Sales.xlsx")
    df['hour'] = pd.to_datetime(df['order_time'], format='%H:%M:%S').dt.hour
    df['month'] = df['order_date'].dt.month
    df = df.rename(columns={'total_price': 'total_sales'})
    return df


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

total_sales = int(df_selection['total_sales'].sum())
total_quantity = int(df_selection['quantity'].sum())
average_sale_by_transaction = round(df_selection['total_sales'].mean(), 2)

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


best_selling_pizza = df.groupby(by=['pizza_name']).sum(numeric_only=True)[['total_sales']].sort_values(by='total_sales', ascending=False).head(5)
fig_best_pizza_sales = px.bar(
    best_selling_pizza,
    y=best_selling_pizza.index,
    x='total_sales',
    orientation='h',
    title="<b>Best selling pizza</b>",
    color_discrete_sequence=["#0083B8"] * len(best_selling_pizza),
    template='plotly_white'
)

fig_best_pizza_sales.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    yaxis=dict(autorange="reversed")
)


worst_selling_pizza = df.groupby(by=['pizza_name']).sum(numeric_only=True)[['total_sales']].sort_values(by='total_sales', ascending=True).head(5)
fig_worst_pizza_sales = px.bar(
    worst_selling_pizza,
    y=worst_selling_pizza.index,
    x='total_sales',
    orientation='h',
    title="<b>Worst selling pizza</b>",
    color_discrete_sequence=["#0083B8"] * len(worst_selling_pizza),
    template='plotly_white'
)

fig_worst_pizza_sales.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    yaxis=dict(autorange="reversed")
)


lefty, righty = st.columns(2)
lefty.plotly_chart(fig_best_pizza_sales, use_container_width=True)
righty.plotly_chart(fig_worst_pizza_sales, use_container_width=True)

sales_by_category = (
    df_selection.groupby(by=['pizza_category']).sum(numeric_only=True)[['total_sales']].sort_values(by='total_sales')
)

fig_product_sales = px.bar(
    sales_by_category,
    x='total_sales',
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


sales_by_hour = df_selection.groupby(by=['hour']).sum(numeric_only=True)[['total_sales']]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y='total_sales',
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

sales_by_month = df_selection.groupby(by=['month']).sum(numeric_only=True)[['total_sales']]
fig_monthly_sales = px.line(
    sales_by_month,
    x=sales_by_month.index,
    y='total_sales',
    title="<b>Sales by month</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_month),
    template='plotly_white'
)

fig_monthly_sales.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(tickmode='linear'),

)

st.plotly_chart(fig_monthly_sales, use_container_width=True)



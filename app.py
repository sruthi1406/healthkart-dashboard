# app.py

import streamlit as st
import plotly.express as px
from utils import load_data, kpi_card
from insights_generator import generate_insights


# Setup
st.set_page_config("📊 HealthKart Influencer Dashboard", layout="wide")
st.title("📈 HealthKart Influencer Campaign Dashboard")

# Load data
influencers, posts, tracking_data, payouts = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
platforms = st.sidebar.multiselect("Select Platforms", tracking_data['source'].unique(), default=tracking_data['source'].unique())
campaigns = st.sidebar.multiselect("Select Campaigns", tracking_data['campaign'].unique(), default=tracking_data['campaign'].unique())

# Apply Filters
filtered_data = tracking_data[
    (tracking_data['source'].isin(platforms)) &
    (tracking_data['campaign'].isin(campaigns))
]

# Generate insights using filtered data
insights = generate_insights(filtered_data, payouts)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", 
    "📉 ROAS & Revenue", 
    "🌟 Top Influencers", 
    "📁 Payout Summary"
])

# === Tab 1: Overview ===
with tab1:
    st.subheader("📊 Campaign KPIs")

    col1, col2, col3 = st.columns(3)
    kpi_card("💰 Total Revenue", insights['total_revenue'], "₹")
    kpi_card("📦 Total Orders", insights['total_orders'])
    kpi_card("📈 Average Order Value", insights['aov'], "₹")

    st.markdown("### 📌 Revenue by Campaign")
    campaign_data = insights['revenue_by_campaign'].reset_index()
    fig_bar = px.bar(campaign_data, x='revenue', y='campaign', orientation='h',
                 labels={'revenue': 'Revenue (₹)', 'campaign': 'Campaign'},
                 title='Revenue by Campaign',
                 color_discrete_sequence=['indigo'])  

    fig_bar.update_layout(height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### 📈 Daily Orders Over Time")
    orders_line = insights['orders_by_date'].reset_index()
    orders_line.columns = ['Date', 'Orders']

    fig_line = px.line(orders_line, x='Date', y='Orders',
                    title='Orders by Day',
                    markers=True,
                    labels={'Orders': 'Total Orders'})
    fig_line.update_layout(height=400)
    st.plotly_chart(fig_line, use_container_width=True)


# === Tab 2: ROAS & Revenue ===
with tab2:
    st.subheader("💸 ROAS Table (Return on Ad Spend)")
    st.dataframe(insights['roas_table'].sort_values(by='ROAS', ascending=False))

# === Tab 3: Top Influencers ===
with tab3:
    st.subheader("🌟 Top 5 Influencers by Revenue")
    st.dataframe(insights['top_influencers'])

# === Tab 4: Payout Summary ===
with tab4:
    st.subheader("📁 Payout Efficiency by Influencer")
    st.dataframe(insights['payout_efficiency'])

    csv = insights['roas_table'].to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download ROAS Report as CSV", data=csv, file_name="roas_report.csv", mime='text/csv')

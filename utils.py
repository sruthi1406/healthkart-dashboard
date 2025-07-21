# utils.py

import pandas as pd
import streamlit as st

def load_data():
    influencers = pd.read_csv("data/influencers.csv")
    posts = pd.read_csv("data/posts.csv")
    tracking_data = pd.read_csv("data/tracking_data.csv")
    payouts = pd.read_csv("data/payouts.csv")
    return influencers, posts, tracking_data, payouts

def kpi_card(title, value, prefix=""):
    st.metric(label=title, value=f"{prefix}{value:,.0f}")

import streamlit as st
import requests
import pandas as pd
import altair as alt

# Set up the currency converter UI
st.set_page_config(page_title="Enhanced Currency Converter", layout="centered", initial_sidebar_state="auto")

# Title and description
st.title("🌍 Enhanced Currency Converter")
st.markdown("Convert currencies quickly and easily. Now with exchange rate trends and history.")

# Set up the API (replace with your actual API key)
API_KEY = '6d11d031b318e43b8475dc32'
url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'

# Caching API data to improve performance
@st.cache_data(ttl=3600)
def get_exchange_rates():
    try:
        response = requests.get(url)
        data = response.json()
        if data['result'] == 'success':
            return data['conversion_rates']
       

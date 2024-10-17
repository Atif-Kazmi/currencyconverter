import streamlit as st
import requests

# Set up the currency converter UI
st.title("Currency Converter")

# Set up the API (replace with your actual API key)
API_KEY = 'YOUR_API_KEY'
url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'

# Use st.cache_data to cache the exchange rates
@st.cache_data
def get_exchange_rates():
    try:
        response = requests.get(url)
        data = response.json()
        if data['result'] == 'success':
            return data['conversion_rates']
        else:
            st.error("Error fetching exchange rates.")
            return None
    except Exception as e:
        st.error(f"Failed to fetch data. {e}")
        return None

# Fetch exchange rates
rates = get_exchange_rates()

if rates:
    # Create input fields for currencies and amount
    amount = st.number_input("Enter amount:", min_value=0.0, format="%.2f")
    from_currency = st.selectbox("From currency", list(rates.keys()), index=list(rates.keys()).index("USD"))
    to_currency = st.selectbox("To currency", list(rates.keys()), index=list(rates.keys()).index("EUR"))

    # Convert the currency
    if st.button("Convert"):
        conversion_rate = rates[to_currency] / rates[from_currency]
        converted_amount = amount * conversion_rate
        st.success(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
else:
    st.warning("Could not load exchange rates. Please try again later.")

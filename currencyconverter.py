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
        else:
            st.error("Error fetching exchange rates.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data. Network issue: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# Get historical data (fake example for demonstration purposes)
@st.cache_data(ttl=3600)
def get_historical_data(currency):
    # Placeholder for historical exchange rate data
    # Replace with actual historical data from an API
    dates = pd.date_range(end=pd.Timestamp.today(), periods=10).to_pydatetime().tolist()
    rates = [1.0 + (i * 0.01) for i in range(10)]  # Simulated rates
    return pd.DataFrame({"Date": dates, "Exchange Rate": rates})

# Fetch exchange rates
rates = get_exchange_rates()

if rates:
    # Create input fields for currencies and amount
    st.sidebar.subheader("Currency Conversion")
    amount = st.sidebar.number_input("Enter amount:", min_value=0.0, format="%.2f", value=1.0)
    from_currency = st.sidebar.selectbox("From currency", list(rates.keys()), index=list(rates.keys()).index("USD"))
    to_currency = st.sidebar.selectbox("To currency", list(rates.keys()), index=list(rates.keys()).index("EUR"))

    # Convert the currency
    conversion_rate = rates[to_currency] / rates[from_currency]
    converted_amount = amount * conversion_rate

    st.sidebar.success(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")

    # Historical data for the selected currency
    st.subheader(f"Historical Exchange Rate for {from_currency} to {to_currency}")
    historical_data = get_historical_data(to_currency)

    # Display line chart of historical data
    chart = alt.Chart(historical_data).mark_line().encode(
        x='Date:T',
        y='Exchange Rate:Q',
        tooltip=['Date:T', 'Exchange Rate:Q']
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

    # Display current exchange rates
    st.subheader(f"Current Exchange Rate: 1 {from_currency} = {conversion_rate:.4f} {to_currency}")
    st.write("Other available currencies:")
    
    # Display data in a table
    rates_df = pd.DataFrame(list(rates.items()), columns=["Currency", "Rate to USD"])
    st.dataframe(rates_df)

else:
    st.warning("Could not load exchange rates. Please try again later.")

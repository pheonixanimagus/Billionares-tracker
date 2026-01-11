import streamlit as st
import requests
import pandas as pd
from sec_api import Form13FHoldingsApi, InsiderTradingApi

# Streamlit app title
st.title("Investment Tracker App")
st.markdown("""
This app allows you to track investments of politicians, billionaires (via insider trades), and hedge funds (via 13F filings).
You need free API keys:
- For politicians: Sign up at https://rapidapi.com/s5yux/api/politician-trade-tracker1 (free tier, no credit card).
- For hedge funds and billionaires: Sign up at https://sec-api.io/ (free tier with 100 calls/day).

Enter your API keys below.
""")

# Input for API keys
rapidapi_key = st.text_input("RapidAPI Key (for Politicians)", type="password")
sec_api_key = st.text_input("SEC-API Key (for Hedge Funds & Billionaires)", type="password")

# Select tracker type
tracker_type = st.selectbox("Select what to track:", ["Politicians", "Billionaires (Insider Trades)", "Hedge Funds (13F Filings)"])

if tracker_type == "Politicians":
    st.subheader("Track Politician Investments")
    politician_name = st.text_input("Enter Politician Name (e.g., Marjorie Taylor Greene):")
    if st.button("Fetch Trades") and rapidapi_key:
        try:
            headers = {
                "X-RapidAPI-Key": rapidapi_key,
                "X-RapidAPI-Host": "politician-trade-tracker1.p.rapidapi.com"
            }
            response = requests.get(
                "https://politician-trade-tracker1.p.rapidapi.com/get_profile",
                headers=headers,
                params={"name": politician_name}
            )
            if response.status_code == 200:
                data = response.json()
                if data:
                    df = pd.DataFrame(data)  # Assuming JSON is list of trades
                    st.dataframe(df)
                else:
                    st.write("No data found.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Exception: {str(e)}")

elif tracker_type == "Billionaires (Insider Trades)":
    st.subheader("Track Billionaire Insider Trades")
    st.markdown("Enter a company trading symbol associated with the billionaire (e.g., TSLA for Elon Musk).")
    symbol = st.text_input("Enter Company Symbol (e.g., TSLA):")
    if st.button("Fetch Insider Trades") and sec_api_key:
        try:
            insider_api = InsiderTradingApi(api_key=sec_api_key)
            query = {"query": f"issuer.tradingSymbol:{symbol.upper()}"}
            response = insider_api.get_data(query)
            transactions = response.get("transactions", [])
            if transactions:
                df = pd.DataFrame(transactions)
                st.dataframe(df)
            else:
                st.write("No insider trades found.")
        except Exception as e:
            st.error(f"Exception: {str(e)}")

elif tracker_type == "Hedge Funds (13F Filings)":
    st.subheader("Track Hedge Fund Holdings")
    st.markdown("""
    Enter the CIK of the hedge fund (Central Index Key from SEC).
    Examples:
    - Berkshire Hathaway (Warren Buffett): 0001067983
    - Bridgewater Associates: 0001350694
    Find CIKs at https://www.sec.gov/edgar/search/
    """)
    cik = st.text_input("Enter Hedge Fund CIK (e.g., 0001350694 for Bridgewater):")
    period = st.text_input("Enter Period of Report (e.g., 2024-03-31):")
    if st.button("Fetch 13F Holdings") and sec_api_key:
        try:
            form13f_api = Form13FHoldingsApi(api_key=sec_api_key)
            query = {
                "query": f"cik:{cik} AND periodOfReport:{period}",
                "from": "0",
                "size": "100",  # Adjust as needed, free tier limits
                "sort": [{"filedAt": {"order": "desc"}}]
            }
            response = form13f_api.get_data(query)
            holdings = response.get("data", [])
            if holdings:
                df = pd.DataFrame(holdings)
                st.dataframe(df)
            else:
                st.write("No holdings found for this CIK and period.")
        except Exception as e:
            st.error(f"Exception: {str(e)}")

st.markdown("""
### How to Run This App
1. Install required packages: `pip install streamlit requests pandas sec-api`
2. Run the app: `streamlit run app.py` (save this code as app.py)
3. Enter your API keys and query away!

Note: Data is based on public filings. Always verify with official sources. Free tiers have limits.
""")

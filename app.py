import streamlit as st
import requests
import pandas as pd
from sec_api import Form13FHoldingsApi, InsiderTradingApi

# ────────────────────────────────────────────────
# App Title & Instructions
# ────────────────────────────────────────────────
st.title("Investment Tracker: Billionaires, Politicians & Hedge Funds")
st.markdown("""
Track recent trades and holdings from:
- **Politicians** (congressional disclosures)
- **Billionaires/Insiders** (Form 4 insider trades)
- **Hedge Funds** (13F quarterly holdings)

**API Keys** are now loaded securely from Streamlit secrets — no need to enter them!
Get your keys from:
- Politicians: https://rapidapi.com/s5yux/api/politician-trade-tracker1
- SEC data: https://sec-api.io (free tier available)
""")

# ────────────────────────────────────────────────
# Load API Keys from secrets (set these in Streamlit Cloud dashboard)
# ────────────────────────────────────────────────
RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY", None)
SEC_API_KEY = st.secrets.get("SEC_API_KEY", None)

if not RAPIDAPI_KEY:
    st.error("RapidAPI Key is missing. Please add RAPIDAPI_KEY to your app secrets in Streamlit Cloud.")
if not SEC_API_KEY:
    st.error("SEC-API Key is missing. Please add SEC_API_KEY to your app secrets in Streamlit Cloud.")

if not (RAPIDAPI_KEY and SEC_API_KEY):
    st.stop()  # Stop execution if keys are missing

# ────────────────────────────────────────────────
# Choose Tracker Type
# ────────────────────────────────────────────────
tracker_type = st.selectbox(
    "What would you like to track?",
    ["Politicians", "Billionaires (Insider Trades)", "Hedge Funds (13F Filings)"]
)

# ────────────────────────────────────────────────
# POLITICIANS SECTION
# ────────────────────────────────────────────────
if tracker_type == "Politicians":
    st.subheader("Politician Stock Trades")
    politician_name = st.text_input("Enter Politician Name", placeholder="e.g., Nancy Pelosi, Marjorie Taylor Greene")

    if st.button("Fetch Trades") and politician_name:
        with st.spinner("Fetching trades..."):
            try:
                headers = {
                    "X-RapidAPI-Key": RAPIDAPI_KEY,
                    "X-RapidAPI-Host": "politician-trade-tracker1.p.rapidapi.com"
                }
                response = requests.get(
                    "https://politician-trade-tracker1.p.rapidapi.com/get_profile",
                    headers=headers,
                    params={"name": politician_name.strip()}
                )
                response.raise_for_status()
                data = response.json()

                if data and isinstance(data, list) and len(data) > 0:
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No trades found for this politician.")
            except requests.exceptions.RequestException as e:
                st.error(f"API Error: {str(e)}")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")

# ────────────────────────────────────────────────
# BILLIONAIRES / INSIDER TRADES SECTION
# ────────────────────────────────────────────────
elif tracker_type == "Billionaires (Insider Trades)":
    st.subheader("Insider Trades (e.g., Elon Musk, Tim Cook)")
    st.markdown("Enter the **company ticker** (e.g., TSLA for Tesla, AAPL for Apple)")
    symbol = st.text_input("Company Ticker", placeholder="TSLA").strip().upper()

    if st.button("Fetch Insider Trades") and symbol:
        with st.spinner("Loading insider transactions..."):
            try:
                insider_api = InsiderTradingApi(api_key=SEC_API_KEY)
                query = {"query": f"issuer.tradingSymbol:{symbol}"}
                response = insider_api.get_data(query)
                transactions = response.get("transactions", [])

                if transactions:
                    df = pd.DataFrame(transactions)
                    # Optional: nicer column order / renaming
                    cols_to_show = ["filingDate", "transactionDate", "ownerName", "ownerTitle",
                                    "transactionType", "shares", "pricePerShare", "securityTitle"]
                    available_cols = [col for col in cols_to_show if col in df.columns]
                    st.dataframe(df[available_cols], use_container_width=True)
                else:
                    st.info(f"No recent insider trades found for {symbol}")
            except Exception as e:
                st.error(f"Error fetching insider trades: {str(e)}")

# ────────────────────────────────────────────────
# HEDGE FUNDS / 13F SECTION
# ────────────────────────────────────────────────
elif tracker_type == "Hedge Funds (13F Filings)":
    st.subheader("Hedge Fund 13F Holdings")
    st.markdown("""
    CIK examples (include leading zeros if needed):  
    - **0001067983** (Berkshire Hathaway – should show ~41 holdings for Q3 2025)  
    - **0001350694** (Bridgewater – hundreds of holdings)  
    Latest period for Berkshire: **2025-09-30** (filed Nov 14, 2025)
    """)

    cik = st.text_input("Hedge Fund CIK", value="0001067983").strip()
    period = st.text_input("Period of Report (YYYY-MM-DD)", value="2025-09-30").strip()

    if st.button("Fetch 13F Holdings") and cik and period:
        with st.spinner("Fetching holdings..."):
            try:
                form13f_api = Form13FHoldingsApi(api_key=SEC_API_KEY)
                query = {
                    "query": f"cik:{cik} AND periodOfReport:\"{period}\"",
                    "from": "0",
                    "size": "50",  # Max allowed
                    "sort": [{"filedAt": {"order": "desc"}}]
                }
                response = form13f_api.get_data(query)
                
                # Debug: Show raw info
                st.caption(f"Raw API response: {len(response.get('data', []))} items found")
                if 'data' in response and response['data']:
                    st.caption(f"First item sample: {response['data'][0]}")
                
                holdings = response.get("data", [])

                if holdings:
                    df = pd.DataFrame(holdings)
                    if 'value' in df.columns:
                        df['value'] = pd.to_numeric(df['value'], errors='coerce')
                        df = df.sort_values('value', ascending=False)
                    
                    key_cols = ['nameOfIssuer', 'titleOfClass', 'value', 'shrsOrPrnAmt', 'investmentDiscretion', 'cusip']
                    avail_cols = [c for c in key_cols if c in df.columns]
                    if len(df) < 5 and len(holdings) > 0:
                        st.warning("API returned few rows — showing full raw data below for debug:")
                        st.json(holdings)  # Show raw list
                    
                    if avail_cols:
                        st.dataframe(df[avail_cols], use_container_width=True, hide_index=True)
                    else:
                        st.dataframe(df, use_container_width=True)
                    
                    st.success(f"Displayed {len(df)} holdings (official: 41 for Berkshire Q3 2025)")
                else:
                    st.info("No holdings data returned. Check API key, period, or try another CIK.")
            except Exception as e:
                st.error(f"API Error: {str(e)}")
# ────────────────────────────────────────────────
# Footer / Notes
# ────────────────────────────────────────────────
st.markdown("---")
st.caption("""
**Notes**:  
• Data comes from public SEC filings & disclosures — always verify with official sources  
• Free API tiers have rate limits  
• Trades/holdings may be delayed (especially 13F: quarterly + 45 days)  
Enjoy tracking! 🚀
""")

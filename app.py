import streamlit as st

# ────────────────────────────────────────────────
# App Title & Description
# ────────────────────────────────────────────────
st.title("Investment Tracker Dashboard")
st.markdown("""
This is a **zero-API, no-key-required** dashboard that links you directly to the  
best free public websites for tracking:

- Politician stock trades  
- Billionaire & executive insider trades  
- Hedge fund 13F holdings  

Click any button — it opens the site in a **new tab**. No login needed.

**Data from public SEC filings** — always up-to-date and reliable.
""")

st.info("Current as of January 2026 — sites may update over time")

# ────────────────────────────────────────────────
# POLITICIANS SECTION
# ────────────────────────────────────────────────
st.header("📜 Politician Stock Trades")
politician_name = st.text_input(
    "Enter politician name",
    placeholder="e.g. Nancy Pelosi, Marjorie Taylor Greene",
    key="politician_input"
).strip()

if politician_name:
    name_encoded = politician_name.replace(" ", "+")
    
    col1, col2 = st.columns(2)
    with col1:
        st.link_button(
            "🔍 Search on CapitolTrades",
            url=f"https://www.capitoltrades.com/politicians?search={name_encoded}",
            use_container_width=True
        )
    with col2:
        st.link_button(
            "🔍 Search on Quiver Quant",
            url=f"https://www.quiverquant.com/congresstrading/search?q={name_encoded}",
            use_container_width=True
        )
else:
    st.caption("Enter a name above to activate the buttons")

# ────────────────────────────────────────────────
# INSIDER TRADES (BILLIONAIRES & EXECUTIVES)
# ────────────────────────────────────────────────
st.header("💼 Insider & Billionaire Trades")
ticker = st.text_input(
    "Enter company ticker",
    placeholder="e.g. TSLA, AAPL, NVDA",
    key="ticker_input"
).strip().upper()

if ticker:
    col3, col4 = st.columns(2)
    with col3:
        st.link_button(
            "🔍 View on InsiderScreener",
            url=f"https://www.insiderscreener.com/en/company/{ticker}",
            use_container_width=True
        )
    with col4:
        st.link_button(
            "🔍 View on Quiver Quant Insiders",
            url=f"https://www.quiverquant.com/insiders/search?ticker={ticker}",
            use_container_width=True
        )
else:
    st.caption("Enter a ticker above to activate the buttons")

# ────────────────────────────────────────────────
# HEDGE FUNDS & 13F HOLDINGS
# ────────────────────────────────────────────────
st.header("🏦 Hedge Fund 13F Holdings")
cik = st.text_input(
    "Enter CIK (include leading zeros)",
    placeholder="e.g. 0001067983 (Berkshire Hathaway)",
    key="cik_input"
).strip()

if cik:
    clean_cik = cik.lstrip('0')  # WhaleWisdom prefers without leading zeros
    
    col5, col6 = st.columns(2)
    with col5:
        st.link_button(
            "🔍 View on WhaleWisdom",
            url=f"https://whalewisdom.com/filer/{clean_cik}",
            use_container_width=True
        )
    with col6:
        st.link_button(
            "🔍 View on Fintel 13F",
            url=f"https://fintel.io/i/{cik}",
            use_container_width=True
        )
else:
    st.caption("Enter a CIK above to activate the buttons")

# Quick examples expander
with st.expander("Popular CIK Examples"):
    st.markdown("""
    - **0001067983** → Berkshire Hathaway (Warren Buffett)  
    - **0001350694** → Bridgewater Associates  
    - **0001364742** → BlackRock  
    - **0000102909** → Vanguard Group  
    """)

# ────────────────────────────────────────────────
# Footer
# ────────────────────────────────────────────────
st.markdown("---")
st.subheader("More Free Resources")
st.markdown("""
- Official SEC EDGAR (raw filings): [https://www.sec.gov/edgar/search](https://www.sec.gov/edgar/search)  
- Unusual Whales Politics: [https://unusualwhales.com/politics](https://unusualwhales.com/politics)
""")

st.caption("Simple, reliable tracking — no more API headaches! 🚀")

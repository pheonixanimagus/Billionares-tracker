import streamlit as st
import webbrowser

# ────────────────────────────────────────────────
# App Title & Description
# ────────────────────────────────────────────────
st.title("Investment Tracker Dashboard")
st.markdown("""
This is a **simple, zero-API, no-key-required** dashboard that helps you quickly access  
the best free public websites to track:

- Politician stock trades  
- Billionaire & executive insider trades  
- Hedge fund 13F holdings  

Just enter the name/ticker/CIK and click — it opens the most relevant pages in new tabs.

**All data comes from public SEC filings & disclosures** — no login, no limits, no rate issues.
""")

st.info("Current as of January 2026 — sites may change layout over time")

# ────────────────────────────────────────────────
# POLITICIANS SECTION
# ────────────────────────────────────────────────
st.header("📜 Politician Stock Trades")
st.caption("Congressional disclosures under the STOCK Act")

politician_name = st.text_input(
    "Politician name",
    placeholder="e.g. Nancy Pelosi, Marjorie Taylor Greene, Dan Crenshaw",
    key="politician"
)

col1, col2 = st.columns(2)

if col1.button("🔍 Search on CapitolTrades", disabled=not politician_name.strip()):
    if politician_name.strip():
        name = politician_name.strip().replace(" ", "+")
        url = f"https://www.capitoltrades.com/politicians?search={name}"
        webbrowser.open_new_tab(url)

if col2.button("🔍 Search on Quiver Quant", disabled=not politician_name.strip()):
    if politician_name.strip():
        name = politician_name.strip().replace(" ", "+")
        url = f"https://www.quiverquant.com/congresstrading/search?q={name}"
        webbrowser.open_new_tab(url)

# ────────────────────────────────────────────────
# INSIDER TRADES (BILLIONAIRES & EXECUTIVES)
# ────────────────────────────────────────────────
st.header("💼 Insider & Billionaire Trades")
st.caption("Form 4 filings — executives, directors, major shareholders")

ticker = st.text_input(
    "Company ticker",
    placeholder="e.g. TSLA, AAPL, NVDA, AMZN",
    key="insider_ticker"
).strip().upper()

col3, col4 = st.columns(2)

if col3.button("🔍 View Insider Trades (InsiderScreener)", disabled=not ticker):
    if ticker:
        url = f"https://www.insiderscreener.com/en/company/{ticker}"
        webbrowser.open_new_tab(url)

if col4.button("🔍 View on Quiver Quant Insiders", disabled=not ticker):
    if ticker:
        url = f"https://www.quiverquant.com/insiders/search?ticker={ticker}"
        webbrowser.open_new_tab(url)

st.caption("Tip: For specific people like Elon Musk, search 'Musk' directly on the sites above")

# ────────────────────────────────────────────────
# HEDGE FUNDS & 13F HOLDINGS
# ────────────────────────────────────────────────
st.header("🏦 Hedge Fund 13F Holdings")
st.caption("Quarterly portfolio snapshots — large investment managers")

cik = st.text_input(
    "CIK number (include leading zeros)",
    placeholder="e.g. 0001067983 (Berkshire), 0001350694 (Bridgewater)",
    key="cik"
).strip()

col5, col6 = st.columns(2)

if col5.button("🔍 View on WhaleWisdom", disabled=not cik):
    if cik:
        clean_cik = cik.lstrip('0')  # WhaleWisdom usually prefers without leading zeros
        url = f"https://whalewisdom.com/filer/{clean_cik}"
        webbrowser.open_new_tab(url)

if col6.button("🔍 View on Fintel 13F", disabled=not cik):
    if cik:
        url = f"https://fintel.io/i/{cik}"
        webbrowser.open_new_tab(url)

# Quick examples
with st.expander("Popular CIK examples"):
    st.markdown("""
    - **0001067983** → Berkshire Hathaway (Warren Buffett)  
    - **0001350694** → Bridgewater Associates  
    - **0001364742** → BlackRock  
    - **0000102909** → Vanguard Group  
    - **0001166691** → Renaissance Technologies  
    """)

# ────────────────────────────────────────────────
# Footer & Additional Resources
# ────────────────────────────────────────────────
st.markdown("---")

st.subheader("Other Useful Free Resources")
st.markdown("""
- **Official SEC EDGAR search** — everything raw:  
  [https://www.sec.gov/edgar/search](https://www.sec.gov/edgar/search)  
- **All politicians combined** (great overview):  
  [https://unusualwhales.com/politics](https://unusualwhales.com/politics)  
- **Top insider trades today**:  
  [https://www.insiderfinance.io/insider-trades](https://www.insiderfinance.io/insider-trades)
""")

st.caption("Enjoy tracking! No APIs = no problems 🚀")

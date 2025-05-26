import streamlit as st
from get_balances import fetch_debank_balances
from csv_utils import append_to_csv, read_csv_data
from scheduler import register_wallet, run_scheduler
import pandas as pd
import os

st.title("DeBank DeFi Balance Tracker")

# Wallet input form
with st.form("wallet_form"):
    wallet = st.text_input("Enter Wallet Address")
    frequency = st.selectbox("Select Frequency", ["Daily", "Weekly", "Monthly"])
    api_key = st.text_input("Enter your DeBank API Key (optional)", type="password")
    submit = st.form_submit_button("Track Wallet")

if submit:
    if api_key:
        os.environ["DEBANK_API_KEY"] = api_key

    st.success(f"Tracking wallet {wallet} ({frequency})")
    balances = fetch_debank_balances(wallet)
    if balances:
        st.write("**Current DeFi Balances:**")
        st.dataframe(pd.DataFrame(balances))
        append_to_csv(wallet, frequency, balances)
        register_wallet(wallet, frequency)
    else:
        st.error("Failed to fetch balances. Check your API key and wallet address.")

# Data Export
if st.button("Export All Data as CSV"):
    df = read_csv_data()
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "wallet_data.csv")

if "scheduler_started" not in st.session_state:
    run_scheduler()
    st.session_state.scheduler_started = True


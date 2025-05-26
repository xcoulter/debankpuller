import csv
import os
import pandas as pd

CSV_FILE = "wallet_data.csv"

def append_to_csv(wallet, frequency, balances):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Wallet Address", "Frequency", "Timestamp", "Token", "Token Balance", "USD Value"])
        for entry in balances:
            writer.writerow([
                wallet,
                frequency,
                entry['timestamp'],
                entry['token'],
                entry['balance'],
                entry['usd_value']
            ])

def read_csv_data():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=["Wallet Address", "Frequency", "Timestamp", "Token", "Token Balance", "USD Value"])
    return pd.read_csv(CSV_FILE)


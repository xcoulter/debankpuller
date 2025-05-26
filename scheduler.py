import schedule
import time
import threading
from get_balances import fetch_debank_balances
from csv_utils import append_to_csv

wallet_registry = []  # In production, persist this

def register_wallet(wallet, frequency):
    wallet_registry.append((wallet, frequency))

def schedule_job(wallet, frequency):
    def job():
        balances = fetch_debank_balances(wallet)
        if balances:
            append_to_csv(wallet, frequency, balances)

    if frequency == "Daily":
        schedule.every().day.at("00:00").do(job)
    elif frequency == "Weekly":
        schedule.every().monday.at("00:00").do(job)
    elif frequency == "Monthly":
        schedule.every(30).days.at("00:00").do(job)

def run_scheduler():
    for wallet, freq in wallet_registry:
        schedule_job(wallet, freq)

    def loop():
        while True:
            schedule.run_pending()
            time.sleep(60)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()

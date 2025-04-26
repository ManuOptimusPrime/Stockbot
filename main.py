import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Details (loaded from .env)
bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Send Hi message when bot starts
def send_startup_message():
    message = "Hi, I am alive! Bot started successfully!"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

# Call this function once at the start
send_startup_message()
# List of stocks to monitor
stocks = ["TATAMOTORS.NS", "BOSCHLTD.NS", "ABB.NS", "PIDILITIND.NS", "INFY.NS"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(url, data=payload)

def check_stocks():
    for stock in stocks:
        url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{stock}?modules=defaultKeyStatistics,financialData"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            try:
                financial_data = data['quoteSummary']['result'][0]['financialData']
                key_stats = data['quoteSummary']['result'][0]['defaultKeyStatistics']

                pe_ratio = key_stats.get('forwardPE', {}).get('raw', 0)
                operating_margin = financial_data.get('operatingMargins', {}).get('raw', 0)
                debt_to_equity = financial_data.get('debtToEquity', {}).get('raw', 100)
                current_ratio = financial_data.get('currentRatio', {}).get('raw', 0)
                profit_margins = financial_data.get('profitMargins', {}).get('raw', 0)

                if (
                    operating_margin > 0.5 and
                    pe_ratio < 100 and
                    profit_margins > 0 and
                    debt_to_equity < 30 and
                    current_ratio > 1
                ):
                    send_telegram(f"✅ {stock} matches Buy Now conditions!")

            except Exception as e:
                print(f"Error parsing {stock}: {e}")
        else:
            print(f"Error fetching data for {stock}")

# Loop forever checking every 15 minutes
while True:
    check_stocks()
    time.sleep(900)  # 900 seconds = 15 minutes

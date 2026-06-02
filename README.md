Binance Futures Testnet Trading Bot



A Python CLI trading bot for Binance Futures Testnet (USDT-M).



&#x20;Project Structure



trading\_bot/

├── bot/

│   ├── \_\_init\_\_.py

│   ├── client.py

│   ├── orders.py

│   ├── validators.py

│   └── logging\_config.py

├── cli.py

├── .env

├── README.md

└── requirements.txt







&#x20;1. Clone the repository

git clone https://github.com/durga-mca/trading_bot.git

cd trading\_bot



&#x20;2. Create virtual environment

python -m venv venv

venv\\Scripts\\activate



3\. Install dependencies

pip install -r requirements.txt



&#x20;4. Configure API keys

Create a .env file:

BINANCE\_API\_KEY=your\_api\_key\_here

BINANCE\_API\_SECRET=your\_api\_secret\_here



&#x20;5. Run the bot

python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 72000







&#x20;Market Order

Symbol     : BTCUSDT

Side       : BUY

Order Type : MARKET

Quantity   : 0.001



&#x20;Limit Order

Symbol     : BTCUSDT

Side       : SELL

Order Type : LIMIT

Quantity   : 0.001

Price      : 72000



Features:



\- Market and Limit orders on Binance Futures Testnet

\- BUY and SELL support

\- Input validation with clear error messages

\- Structured logging to file and console

\- Exception handling for API and network errors

\- Paper trading mode with real Binance price feeds



&#x20;Assumptions and Notes :



Note: Binance Futures Testnet restricts API access for Indian users without KYC verification. This bot is fully built for Binance Futures Testnet (https://testnet.binancefuture.com). Log files are generated using paper trading mode with real Binance Futures price feeds.

The code is 100% compatible with real Binance Futures Testnet API when API keys are available.



Requirements:



\- Python 3.x

\- requests

\- python-dotenv


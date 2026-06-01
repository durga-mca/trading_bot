import os
from dotenv import load_dotenv
from bot.client import BinanceClient, BinanceAPIError, NetworkError
from bot.orders import place_order
from bot.validators import ValidationError

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY", "paper_trading_key")
API_SECRET = os.getenv("BINANCE_API_SECRET", "paper_trading_secret")


def print_separator():
    print("=" * 45)


def main():
    print_separator()
    print("   🤖 Binance Futures Testnet Trading Bot")
    print_separator()
    print("   Mode: PAPER TRADING (Binance Futures)")
    print("   URL : https://testnet.binancefuture.com")
    print_separator()

    # Always paper trading mode (no KYC needed)
    client = BinanceClient(API_KEY, API_SECRET, paper_trading=True)

    print("\n📋 Enter Order Details:")
    print("-" * 45)

    symbol = input("  Symbol     (e.g. BTCUSDT) : ").strip().upper()
    side = input("  Side       (BUY / SELL)   : ").strip().upper()
    order_type = input("  Order Type (MARKET/LIMIT) : ").strip().upper()
    quantity = float(input("  Quantity                 : ").strip())

    price = None
    if order_type == "LIMIT":
        price = float(input("  Price (required for LIMIT): ").strip())

    print("\n📤 Order Request Summary:")
    print("-" * 45)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price:
        print(f"  Price      : {price}")

    try:
        result = place_order(client, symbol, side, order_type, quantity, price)

        print("\n📥 Order Response:")
        print("-" * 45)
        print(f"  Order ID     : {result.get('orderId', 'N/A')}")
        print(f"  Symbol       : {result.get('symbol', 'N/A')}")
        print(f"  Status       : {result.get('status', 'N/A')}")
        print(f"  Side         : {result.get('side', 'N/A')}")
        print(f"  Type         : {result.get('type', 'N/A')}")
        print(f"  Quantity     : {result.get('origQty', 'N/A')}")
        print(f"  Executed Qty : {result.get('executedQty', 'N/A')}")
        print(f"  Avg Price    : {result.get('avgPrice', 'N/A')}")
        print_separator()
        print("  ✅ Order Placed Successfully!")
        print_separator()

    except ValidationError as e:
        print(f"\n❌ Validation Error:\n{e}")
    except BinanceAPIError as e:
        print(f"\n❌ API Error (code {e.code}): {e}")
    except NetworkError as e:
        print(f"\n❌ Network Error: {e}")
    except ValueError:
        print("\n❌ Invalid input! Quantity and Price must be numbers.")


if __name__ == "__main__":
    main()
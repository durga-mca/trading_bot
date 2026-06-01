import os
import argparse
from dotenv import load_dotenv
from bot.client import BinanceClient, BinanceAPIError, NetworkError
from bot.orders import place_order
from bot.validators import ValidationError

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY", "paper_trading_key")
API_SECRET = os.getenv("BINANCE_API_SECRET", "paper_trading_secret")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet Trading Bot (USDT-M)",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001\n"
            "  python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 72000\n"
        )
    )
    parser.add_argument("--symbol",   required=True,  help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side",     required=True,  choices=["BUY", "SELL"], type=str.upper, help="BUY or SELL")
    parser.add_argument("--type",     required=True,  choices=["MARKET", "LIMIT"], type=str.upper, dest="order_type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True,  type=float, help="Order quantity, e.g. 0.001")
    parser.add_argument("--price",    required=False, type=float, default=None, help="Limit price (required for LIMIT orders)")
    return parser


def print_separator():
    print("=" * 45)


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Extra validation: price required for LIMIT
    if args.order_type == "LIMIT" and args.price is None:
        parser.error("--price is required for LIMIT orders")

    print_separator()
    print("   🤖 Binance Futures Testnet Trading Bot")
    print_separator()
    print("   Mode: PAPER TRADING (Binance Futures)")
    print("   URL : https://testnet.binancefuture.com")
    print_separator()

    print("\n📤 Order Request Summary:")
    print("-" * 45)
    print(f"  Symbol     : {args.symbol.upper()}")
    print(f"  Side       : {args.side}")
    print(f"  Type       : {args.order_type}")
    print(f"  Quantity   : {args.quantity}")
    if args.price:
        print(f"  Price      : {args.price}")

    client = BinanceClient(API_KEY, API_SECRET, paper_trading=True)

    try:
        result = place_order(client, args.symbol, args.side, args.order_type, args.quantity, args.price)

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
import yfinance as yf
import pandas as pd
import ta
import sys
import logging

def main():
    print("Welcome to the Stock Trading Bot")
    symbol = input("Enter the stock symbol you want to analyze. ").upper()

    data = fetch_data(symbol)
    if data is None:
        return

    analysis, atr_value = analyze(data)

    action = user_action(analysis)

    stock_price, stop_loss, take_profit, quantity = execute(action, symbol, atr_value)

    print(f"\nExecuting trade: {action} ${quantity} worth of shares")
    print(f"Entry stock price: {stock_price}")
    print(f"Take Profit set at {take_profit:.2f}")
    print(f"Stop Loss set at {stop_loss:.2f}")
    print("Trade Succesfull! (Simulation)")


def fetch_data(symbol):
    logging.getLogger("yfinance").setLevel(logging.CRITICAL)

    try:
        data = yf.download(symbol, period="6mo", interval="1d", auto_adjust=False)
        if data.empty:
            raise ValueError(f"\nNo available data for this stock. Please try another symbol.")

        # Flatten MultiIndex to single-level columns for easier referencing
        data.columns = [col[0] for col in data.columns]

        data["ATR"] = ta.volatility.AverageTrueRange(high=data["High"], low=data["Low"], close=data["Close"], window=14).average_true_range()

        return data
    except Exception as e:
        print(f"Error retrieving stock data: {e}")
        return None


def analyze(data):
    data["SMA50"] = data["Close"].rolling(window=50).mean()

    close_prices = data[["Close"]].squeeze()

    rsi_indicator = ta.momentum.RSIIndicator(close_prices)
    data["RSI"] = rsi_indicator.rsi().fillna(0)

    data = data.dropna(subset=["SMA50", "RSI", "Close"], how="any")

    last_row = data.iloc[-1]
    sma_trend = "above" if last_row["Close"] > last_row["SMA50"] else "below"
    rsi_value = last_row["RSI"]
    atr_value = last_row["ATR"] if "ATR" in data.columns else 0

    print("\n----- Stock Analysis -----")
    print(f"Current price: {last_row['Close']:.2f}")
    print(f"RSI Value: {rsi_value:.2f}")
    print(f"The stock is trading {sma_trend} its 50-day moving average.")
    if rsi_value < 25:
        print("The RSI indicate the stock might be oversold (RSI < 25).")
    elif rsi_value > 75:
        print("The RSI indicates the stock might be overbought (RSI > 75).")
    else:
        print("The RSI is neutral (25 <= RSI <= 75)")

    print(f"ATR Value: {atr_value:.2f}")

    return last_row, atr_value


def user_action(analysis):
    user_choice = input("\nDo you want to execute a trade based on the analysis given (yes/no)? ").lower()
    if user_choice == "yes" or user_choice =="y":
        if analysis["RSI"] < 25:
            return "BUY"
        if analysis["RSI"] > 75:
            return "SELL"
        else:
            sys.exit("Trading signals are not strong enough. Trade not executed.")

    else:
        sys.exit("Thank you for using the Stock Trading Bot!")


def execute(action, symbol, atr_value):
    quantity = int(input(f"{symbol} shares worth of how much USD do you want to {action}? $"))
    stock = yf.Ticker(symbol)
    stock_price = stock.info["currentPrice"]
    stop_loss = sl_level(atr_value, stock_price, action)
    take_profit = tp_level(action, atr_value, stock_price)
    return stock_price, stop_loss, take_profit, quantity


def tp_level(action, atr_value, stock_price):
    if action == "BUY":
        return stock_price + 2 * atr_value
    elif action == "SELL":
        return stock_price - 2 * atr_value


def sl_level(atr_value, stock_price, action):
    if action == "BUY":
        return stock_price - atr_value
    elif action =="SELL":
        return stock_price + atr_value


if __name__ == "__main__":
    main()

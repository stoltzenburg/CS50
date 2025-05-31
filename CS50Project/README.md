# Stock trading Bot

#### Video Demo:  https://youtu.be/yP_KRozBC6w

## Overview

The **Stock Trading Bot** is a Python-based tool designed to help users analyze stock market data and make informed trading decisions
based on technical indicators. This bot utilizes the **yfinance** library to retrieve stock data and the **ta** library to compute key
indicators such as the 50-day Simple Moving Average (SMA), Relative Strength Index (RSI), and Average True Range (ATR). Based on this
analysis, the bot suggests trading actions and simulates trade execution, including setting stop-loss and take-profit levels.

## Features

The bot fetches stock data for a six-month period and calculates key technical indicators to provide a comprehensive analysis. It
determines trade actions based on the RSI value, allowing the user to decide whether to proceed with a trade. The program then simulates
the trade execution by providing an entry price, stop-loss level, and take-profit level. The entire process is conducted through a
simple command-line interface that interacts with the user.

## File Structure

The `main()` function serves as the entry point of the program. It welcomes the user and prompts for a stock symbol, then proceeds to
fetch stock data, analyze trends, determine user action, and execute a simulated trade. The `fetch_data()` function is responsible
for retrieving historical stock data using `yfinance`. It also computes the **ATR** to measure market volatility and ensures that any
invalid or unavailable stock symbols are handled appropriately. The function returns a **pandas DataFrame** containing stock data with
the necessary indicators.

The `analyze()` function calculates the **50-day SMA** and **RSI**, while also determining if the stock price is above or below its
50-day moving average. Additionally, it checks whether the RSI suggests an overbought or oversold condition and prints a summary of the
stock analysis. The last row of the dataset and ATR value are returned for trade execution.

The `user_action()` function prompts the user to decide whether to trade based on the analysis provided. If the RSI suggests
that the market is oversold, the function recommends a **BUY** action. On the other hand, if the RSI indicates an overbought market, a
**SELL** action is suggested. If the trading signals are weak, the program exits.

The `execute()` function prompts the user to specify how much they want to trade in USD. It then fetches the
current stock price using `yfinance`, calculates the stop-loss and take-profit levels using the ATR value, and displays the details of
the simulated trade. The `tp_level()` function calculates the take-profit level based on the trade action,
while the `sl_level()` function determines the stop-loss level.

## Design Choices

The bot relies on well-established technical indicators to inform trading decisions. The **RSI** helps identify overbought and oversold
conditions, while the **SMA** provides trend direction. The **ATR** measures market volatility, which is used to determine stop-loss and
take-profit levels. By incorporating these indicators, the bot offers a structured approach to stock analysis without requiring
extensive user input.

Instead of executing trades automatically, the bot requires user confirmation before proceeding. This design choice prevents unintended
trades and ensures that users remain in control of their decisions. Furthermore, since the program operates in a simulated environment,
users can assess trade outcomes without financial risk.

## Prerequisites

To run the Stock Trading Bot, users must have the following Python libraries installed: `yfinance`, `pandas`, `ta`, `sys`, and
`logging`. Missing dependencies can be installed using the command `pip install yfinance pandas ta`.

## Running the Program

The bot can be started by running the command `python project.py` in the terminal. Users will then be prompted to enter the stock symbol
they wish to analyze and follow the instructions provided by the bot.

## Future Enhancements

Several potential improvements can be made to the bot. Integrating with a brokerage API such as Alpaca or Interactive Brokers would
allow real trade execution. Adding additional technical indicators, could improve the accuracy of trade signals. Developing a graphical
user interface (GUI) using Tkinter or a web-based dashboard would enhance user experience and visualization.

## Conclusion

The Stock Trading Bot provides an accessible and effective way to analyze stocks using technical indicators. By offering insights based
on RSI, SMA, and ATR values, the bot enables users to make informed trade decisions. Its ability to simulate trade execution with
calculated stop-loss and take-profit levels makes it a valuable tool for both beginner and experienced traders.

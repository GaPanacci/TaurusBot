# Taurus Bot

## Overview
Taurus Bot is a Python-based automated trading bot designed to execute buy and sell orders on the stock market based on the Simple Moving Average (SMA) strategy. Using the Alpaca API for market data and trading actions, Taurus Bot aims to assist users in capitalizing on market movements without manual intervention. 

## Features
- **Automated Trading:** Executes buy and sell orders based on SMA indicators.
- **Market Time Awareness:** Operates only during market hours to ensure compliance with trading regulations.
- **User Customization:** Allows users to specify the stock symbol and the quantity of stocks they wish to trade.

## Prerequisites
To use Taurus Bot, you need:
- An Alpaca account with API keys (API key and secret key).
- Python 3.6 or later installed on your system.

## Setup and Installation
1. **Clone the Repository:**
   - Use `git clone` or download the zip file of the Taurus Bot repository to your local machine.
2. **Install Dependencies:**
   - Install Python dependencies required by Taurus Bot by running:
     ```
     pip install alpaca-trade-api pandas
     ```
3. **Configure API Keys:**
   - Open the Taurus Bot script in a text editor.
   - Replace the placeholder values for `api_key` and `secret_key` with your Alpaca account's API keys.

## Usage
1. **Configure Trading Parameters:**
   - When you run Taurus Bot, it will prompt you to enter the stock symbol you wish to trade and the quantity of stocks for each transaction.
2. **Run the Bot:**
   - Execute the script in your terminal or command prompt:
     ```
     python taurus_bot.py
     ```
   - Follow the on-screen prompts to initiate trading.

## Important Notes
- Taurus Bot trades based on the SMA strategy, which may not suit all market conditions or individual trading preferences. 
- Ensure you understand the risks involved in automated trading and the specific characteristics of the stocks you choose to trade.

## Contribution
Feedback, contributions, and feature requests are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

## Disclaimer
Taurus Bot is provided "as is", without warranty of any kind. Use it at your own risk. The developers are not responsible for any financial losses incurred while using the bot. Ensure you have adequate understanding of the stock market and automated trading before use.

## License
This project is open-source and available under the MIT License. See the LICENSE file for more details.
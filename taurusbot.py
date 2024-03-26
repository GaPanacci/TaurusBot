
from time import sleep
from datetime import datetime, timedelta
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient

# Initial global variable declarations
current_time, start_time, end_time = None, None, None

# Set API keys and initialize variables
api_key = "Enter API Key Here"
secret_key = "Enter Secret Key Here"

# Prompt user for the stock symbol they wish to trade
stock_choice = input("Please enter the stock symbol you would like to trade: ")

# Initialize stock_quantity to None, will prompt user until a valid number is provided
stock_quantity = None

# Loop to ensure user inputs a valid stock quantity
while stock_quantity is None:
    try:
        stock_quantity_input = input(f"How many {stock_choice} stocks would you like to buy and sell at once? ")
        stock_quantity = int(stock_quantity_input)
        if stock_quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
    except ValueError as error:
        print(f"Invalid input: {error}. Please try again.")

        stock_quantity = None

# Initialize trading and data clients
client = StockHistoricalDataClient(api_key, secret_key)
trading_client = TradingClient(api_key, secret_key, paper=True)

# Define market operation times
market_open = datetime.now().replace(hour=9, minute=30, second=0, microsecond=0)
last_call = datetime.now().replace(hour=15, minute=45, second=0, microsecond=0)
market_close = datetime.now().replace(hour=16, minute=00, second=0, microsecond=0)

# Display welcome message
print("""-----------------------------------------------------------
Taurus is starting up...
-----------------------------------------------------------""")

# Function to update current, start, and end times for data fetching
def time_check():
    global current_time, start_time, end_time

    current_time = datetime.now().replace(second=0, microsecond=0)
    start_time = current_time - timedelta(minutes=13)
    end_time = current_time

time_check()

# Function to get the current number of positions held
def get_position():
    positions = trading_client.get_all_positions()
    if positions:
        return sum(int(pos.qty) for pos in positions)
    return 0


# Function to fetch and return data for the specified stock
def data_scrape():
    try:
        request_params = StockBarsRequest(
            symbol_or_symbols=[stock_choice],
            timeframe=TimeFrame.Minute,
            start=start_time,
            end=end_time
        )
        bars = client.get_stock_bars(request_params)
        df = bars.df[['close']]
        return df

    except Exception as fetch_error:
        print(f"Failed to fetch stock bars: {fetch_error}")
        return None

# Function to calculate and return simple moving average indicators
def sma_indicator(df):

    # Calculate the SMA for the most recent 5 minutes
    sma_5 = round(float(df['close'].iloc[-5:].mean()), 3)

    # Calculate the SMA for all 13 minutes
    sma_13 = round(float(df['close'].iloc[-13:].mean()), 3)

    if sma_5 > sma_13:
        return 1
    elif sma_5 == sma_13:
        return 0
    else:
        return -1

# Functions to place buy or sell orders
def buy_stocks():
    try:
        market_order_data = MarketOrderRequest(
            symbol=stock_choice,
            qty=stock_quantity,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.GTC
        )
        trading_client.submit_order(order_data=market_order_data)
    except Exception as buy_error:
        print(f"Failed to submit buy order: {buy_error}")

def sell_stocks():
    try:
        market_sales_data = MarketOrderRequest(
            symbol=stock_choice,
            qty=stock_quantity,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.GTC
        )
        trading_client.submit_order(order_data=market_sales_data)
    except Exception as sell_error:
        print(f"Failed to submit sell order: {sell_error}")

# Function to calculate the next run time based on a given interval
def calculate_next_run(interval_seconds):
    now = datetime.now()
    additional_seconds = interval_seconds - (now.second % interval_seconds) - (now.microsecond / 1_000_000.0)
    return now + timedelta(seconds=additional_seconds)

# Function to liquidate all positions before the market closes
def liquidate_positions():
    if get_position() > 0:
        sell_stocks()
        print("Closing all open positions before market close.")


# Main logic
interval_second = 60
while True:
    try:
        current_time = datetime.now().replace(second=0, microsecond=0)
        if market_open < current_time < last_call:
            time_check()
            market_data_df = data_scrape()
            if market_data_df is None:
                continue
            indicator = sma_indicator(market_data_df)
            position_qty = get_position()

            if indicator == 1 and position_qty > 0:
                print("SMA indicator favourable.\nMaximum {} positions reached.\nYou still have an open {} position.".format(
                    stock_choice, stock_choice))
                print("Time check: {} \n-----------------------------------------------------------".format(current_time))

            elif indicator == 1 and position_qty == 0:
                buy_stocks()
                print("SMA indicator favourable.\nYou have purchased an {} position.\nYou now have an open {} position.".format(
                    stock_choice, stock_choice))
                print("Time check: {} \n-----------------------------------------------------------".format(current_time))

            elif indicator == 0 and position_qty > 0:
                print("SMA indicator neutral.\nNo further action required.\nYou still have an open {} position.".format(
                    stock_choice))
                print("Time check: {} \n-----------------------------------------------------------".format(current_time))

            elif indicator == 0 and position_qty == 0:
                print("SMA indicator neutral.\nNo further action required.\nYou do no have any open {} positions.".format(
                    stock_choice))
                print("Time check: {} \n-----------------------------------------------------------".format(current_time))

            elif indicator == -1 and position_qty == 0:
                print("SMA indicator unfavourable.\nNo further action required.\nYou do no have any open {} positions.".format(
                    stock_choice))
                print("Time check: {} \n-----------------------------------------------------------".format(current_time))

            else:
                sell_stocks()
                print("SMA indicator unfavourable.\nYou have sold an {} position.\nYou now have no open {} positions.".format(
                    stock_choice, stock_choice))
                print("Time check: {} \n-----------------------------------------------------------".format(current_time))

    except Exception as loop_errors:
        print(f"An error occurred during the main loop: {loop_errors}")

    finally:

        next_run = calculate_next_run(interval_second)
        sleep_duration = (next_run - datetime.now()).total_seconds()
        sleep(max(0, sleep_duration))

        current_time = datetime.now().replace(second=0, microsecond=0)
        if last_call < current_time < market_close:
            liquidate_positions()
            print(f"Market is closing soon. Attempted to close positions at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            break  # Exit the loop since the market is about to close

print("-----------------------------------------------------------\n ")
print(f"Taurus is shutting down. All positions are intended to be closed as of {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
print("-----------------------------------------------------------")

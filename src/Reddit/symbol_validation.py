import pandas as pd

#all_stocks_symbols = pd.read_csv("./src/Reddit/assets/stocks_info.csv")['Symbol'].to_list()
all_stocks_symbols = pd.read_csv("assets/stocks_info.csv")['Symbol'].to_list()

def is_that_a_stock(symbol):
    if symbol in all_stocks_symbols:
        return True
    return False


if __name__ == "__main__":
    ex = ['AAPL', 'LOL', 'FGGW', "ASS", "TFW"]
    for symbol in ex:
        print(is_that_a_stock(symbol))

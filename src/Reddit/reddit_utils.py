import pandas as pd
import reticker as rt

all_stocks_symbols = pd.read_csv("./src/Reddit/assets/stocks_info.csv")['Symbol'].to_list()

def is_that_a_stock(symbol):
    if symbol in all_stocks_symbols:
        return True
    return False

def base36encode(integer: int) -> str:
	chars = '0123456789abcdefghijklmnopqrstuvwxyz'
	sign = '-' if integer < 0 else ''
	integer = abs(integer)
	result = ''
	while integer > 0:
		integer, remainder = divmod(integer, 36)
		result = chars[remainder] + result
	return sign + result


def base36decode(base36: str) -> int:
	return int(base36, 36)


if __name__ == "__main__":
	c = "$PICK is cheap because its constituent stocks."
	possible_symbols = rt.TickerExtractor().extract(c)
	print(possible_symbols)
	for symbol in possible_symbols:
		print(is_that_a_stock(symbol=symbol))

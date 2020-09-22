from sys import path
from os.path import dirname

path.append(dirname(path[0]))
from Help_functions._bot_functions import _prices_helper, _converting_raw_price_to_float, _update_auctions_prices_from_csv
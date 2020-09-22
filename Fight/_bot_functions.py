from sys import path
from os.path import dirname

path.append(dirname(path[0]))
from Help_functions._bot_functions import _fighting, _random_sleep, _get_battle_id, _fix_product_name

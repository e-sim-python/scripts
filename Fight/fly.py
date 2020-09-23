from sys import path
from os.path import dirname

path.append(dirname(path[0]))
from Basic.fly import fly

# E-sim python library
[![Flag Counter](https://s01.flagcounter.com/mini/5j6R/bg_FFFFFF/txt_000000/border_CCCCCC/flags_0/)](https://info.flagcounter.com/5j6R)

## You always wanted to use automated software, but did not have the necessary knowledge?
### Here are few examples:
- Auto-fight every restore.
- Bid on all auctions with a single click
- Dump all limits with a single click.
- Complete all the missions with a single click.
- Auto-hunt BHs
- Discord bot (control each of your trusted group accounts via commands)
- And much more!

(As far as we know, no one has ever been punished for using those scripts. However, the use is at your own risk, of course.)

This project is open-source, so anyone can check any line and see if it's harmful.
Everything written is pretty much plain English, so you can see search for traps, and what each code really does.
If you still think there is a suspicious line, you can [ask us about it, and warn other users as well](https://github.com/e-sim-python/scripts/issues)

### Usage:
- Download and Install [python 3.6+](https://www.python.org/downloads/) and [add to path](http://prntscr.com/uwvy5z). (Android users click [here](https://github.com/e-sim-python/scripts/issues/2#issuecomment-698446627)).
- Download the e-sim library as a zip file ([Code -> download ZIP](https://github.com/e-sim-python/scripts/archive/master.zip)) and extract it. (If you can't extract, [download WinRAR](https://www.rarlab.com/) first)
- At the first run, you will have to execute [install_packets.py](https://github.com/e-sim-python/scripts/blob/master/Help_functions/install_packets.py), or install `aiohttp` and `lxml` manually (type `CMD` at your start menu, and `py -m pip install aiohttp` at your CMD). ([More help for this step](https://packaging.python.org/tutorials/installing-packages/))
- Double click (in your computer) on any script you want, or right click -> open with IDLE.
- Alternative (advanced): import the function to another script ([examples](https://github.com/e-sim-python/scripts/blob/master/bot.py)).

### Few notes:
- You can edit the scripts by right click on it -> edit with IDLE, or click "Fork" at the top of this page.
- Everything written after the pound (#) in the same line, is a note that can help you understand the code, or for the developers.
- Every line with `input` can be replaces (instead of typing the same choice every time you run the script). For example: `server = input("Server: ")` can be replaced into `server = "alpha"`.

Those scripts (Basic folder mainly) are mostly raw, and they can be used in many other ways.

**Beginner idea:**
- Add `await asyncio.sleep(time_in_sconds)` at the beginning of the script to do action with a delay (For example: Bid auctions just before it's end, propose a law while you are sleeping etc.)

**Advanced idea:**
- Run the [discord bot](https://github.com/e-sim-python/scripts/blob/master/bot.py) in each of your trusted group devices, and let everyone do specific actions in each other accounts (fight, vote laws etc.) (you will have to install `discord.py`)
- Alternative, you can do that with multies and VPS ;)

### Errors:
- First try to search for solution online.
- For example: `ImportError: No module named aiohttp` -> [google search](https://www.google.com/search?q=No+module+named+aiohttp) will tell you how to install packet (via pip). In that specific error you can also run [install_packets.py](https://github.com/e-sim-python/scripts/blob/master/Help_functions/install_packets.py)
- Sometimes all you need is to login via script again, because your cookies are too old.
- See if there are updates in the code source.
- If you believes that the error is made by us, you can describe it [here](https://github.com/e-sim-python/scripts/issues) and we will try to fix. This is also the place for suggestions and any contact.

# Good luck & have fun!

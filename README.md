
# E-sim python library
[![Flag Counter](https://s01.flagcounter.com/mini/5j6R/bg_FFFFFF/txt_000000/border_CCCCCC/flags_0/)](https://info.flagcounter.com/5j6R)
##### Table of Content:
1. [Introduction](https://github.com/e-sim-python/scripts#introduction)
2. [Installation and usage](https://github.com/e-sim-python/scripts#installation-and-usage)
	1. [Installation]()
		1. [PC]()
			1. [Installing]()
			2. [Usage]()
		2. [Android]()
	3. [Notes]()
	4. [Customization and Advanced usage]()
4. [Troubleshooting]()

## Introduction
#### You always wanted to use automated software, but did not have the necessary knowledge?
- #### Here are few examples:
	- Auto-fight every hp restore.
	- Bid on all auctions with a single click
	- Dump all limits with a single click.
	- Complete all the missions with a single click.
	- Auto-hunt BHs
	- Discord bot (control each of your trusted group accounts via commands)
	- And much more!
---
Currently there are 2 available versions of these scripts, which both of them does the same thing, but the lastest version is using **Asyncio** and **AIOHTTP** Library which is a non-blocking version of previous release for Discord bot usage, you can access both versions from this Link : [**Releases**](https://github.com/e-sim-python/scripts/releases)

As far as we know, no one has ever been punished for using these scripts. However, the use is at your own risk, of course.

**This project is open-source, so anyone can check any line and see if it's harmful.
Everything written is pretty much plain English, so you can see search for traps, and understand what each code really does.
If you still think there is a suspicious line, you can [ask us about it, and warn other users as well](https://github.com/e-sim-python/scripts/issues)**

## Installation and usage:
- ### Installation:
	- #### PC Users:
		- #### Installing:
			1. Download and Install [python 3.6+](https://www.python.org/downloads/) and [add to path](http://prntscr.com/uwvy5z). 
			2. Open your CMD ( Command Line ), type `pip install eSim` then press enter and wait for everything to get installed on your computer.
			3. Download the e-sim library as a zip file ([Code -> download ZIP](https://github.com/e-sim-python/scripts/archive/master.zip)) and extract it. (If you can't extract, [download WinRAR](https://www.rarlab.com/) first)
		- #### Usage:
			- Head back to the folder you extracted in Step 2, `Double click (in your computer) on any script you want`, or right click -> `open with IDLE` and `Press F5` or from `Run Menu` select `Run Module`
			- *advanced usage* : import the function to another script ([examples](https://github.com/e-sim-python/scripts/blob/master/bot.py)).
	
	- #### Android users:
		1. Download the e-sim library as a zip file on your Android device from [Here](https://github.com/e-sim-python/scripts/releases) : [**Download Link**](https://github.com/e-sim-python/scripts/archive/aee27a71a54e8e7e2fc2b660611e122fe354fbe7.zip)
		2. Extract the downloaded zip file.
		3. Install **Pydroid 3 - IDE for Python 3** from Google Play Store.
		
		4. Install **Pydroid repository plugin** from Google Play Store.
		
		5. Open **Pydroid 3**, from top left side of app, click on menu, there are a few options, such as Get premium, interpreter, Terminal, etc,Now you should choose **Pip**.
		
		6. In **Library name** field, first type **lxml** (its LXML not ixmi) and click on install, after its finished, enter **Requests** in that field and go ahead and click install. ( you can do this for any missing module in future if you needed it)
		
		7. Now, just go back in main menu and click on folder icon in top right side of the app ( near light bulb icon ) and choose open, find your desired script in your phone file manager and open it.

		8. Once you opened it, there should be a **Run yellowish play button** in left bottom of screen, go ahead and run it.
		9. Now after you ran the script in your phone, on top right side of the screen, there is a menu. In that menu, choose **Take wakelock** and **Take wifilock**, Now it should be able to run as long as you don't close the app from your phone's app manager. [Screenshot](http://prntscr.com/uo9dxh)


- ### Few Notes:
	- You can edit the scripts by right click on it -> edit with IDLE, or click "Fork" at the top of this page.
	- Everything written after the pound (#) in the same line, is a note that can help you understand the code, or for the developers.
	- Every line with `input` can be replaces (instead of typing the same choice every time you run the script). For example: `server = input("Server: ")` can be replaced into `server = "alpha"`.
	- Those scripts (Basic folder mainly) are mostly raw, and they can be used in many other ways.
	- in [Discord bot](https://github.com/e-sim-python/scripts/blob/master/bot.py), if you want to run command in a specific server, **Channel name should be the same as the server you want to run the command on**. ( Ex: if it you wish to run command in alpha server, name of channel should be `alpha`)
- ### Customization and Advanced usage:
	- **Beginner idea:**
		- Add `await asyncio.sleep(time_in_sconds)` at the beginning of the script to do action with a delay (For example: Bid auctions just before it's end, propose a law while you are sleeping etc.)

	- **Advanced idea:**
		- Run the [discord bot](https://github.com/e-sim-python/scripts/blob/master/bot.py) in each of your trusted group devices, and let everyone do specific actions in each other accounts (fight, vote laws etc.) (you will have to install `discord.py`)
		- you can do that with multies and VPS ;)
		
## Troubleshooting:
- Make sure that you have python 3.6+ installed by typing `python --version` or `py --version` in CMD. [SCREENSHOT](http://prntscr.com/wmrbkn)
- First try to search for the solution online.
- For example: `ImportError: No module named aiohttp` -> [google search](https://www.google.com/search?q=No+module+named+aiohttp) will tell you how to install packet (via pip). In that specific error you can also run [install_packets.py](https://github.com/e-sim-python/scripts/blob/master/Help_functions/install_packets.py)
- Sometimes all you need is to login via script again, because your cookies are too old.
- See if there are updates in the source code.
- If you believes that the error is made by us, you can describe it [here](https://github.com/e-sim-python/scripts/issues) and we will try to fix. This is also the place for suggestions and any contact.


# Good luck & have fun!

import discord
from discord.ext import commands
from io import StringIO
from contextlib import redirect_stdout
from collections import defaultdict

from Basic import *
from Fight import *
from Time_saver import *
from login import get_nick_and_pw


bot = commands.Bot(command_prefix = ".", case_insensitive=True)
YOUR_SECRET_TOKEN = input("Your discord token (help - https://www.writebots.com/discord-bot-token/): ")

sessions = defaultdict(lambda: "")

# MY_NICKS = {"secura": "Some Nick",
#             "suna": "Another Nick"}
MY_NICKS = get_nick_and_pw("all")


@bot.event
async def on_ready():  
    print('Logged in as')    
    print(bot.user.name)


def add_docs_for(other_func):  
    def dec(func):
        if not other_func.__doc__:
            other_func.__doc__ = ""
        if not func.__doc__:
            func.__doc__ = ""
        func.__doc__ = other_func.__doc__ + "\n\n" + func.__doc__
        return func
    return dec


@bot.command()
@add_docs_for(accept_contract.accept_contract)
async def accept(ctx, contract_id, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = accept_contract.accept_contract(server, contract_id, session)

@bot.command()
@add_docs_for(battle_order.battle_order)
async def bo(ctx, battle_link, side, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = battle_order.battle_order(server, battle_link, side, session)

@bot.command()
@add_docs_for(bid.bid_specific_auction)
async def bid(ctx, auction_id_or_link, price, delay, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        if delay.lower() not in ("yes", "no"):
            await ctx.send(f"delay parameter must to be 'yes' or 'no' (not {delay})")
            return
        else:
            delay = True if delay.lower() == "yes" else False
        session = sessions[server]
        sessions[server] = bid.bid_specific_auction(server, auction_id_or_link, price, delay, session)

@bot.command()
@add_docs_for(buff.buffs)
async def buff(ctx, buffs_names, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = buff.buffs(server, buffs_names, session)
        

@bot.event                                          
async def on_message(message):
    ctx = await bot.get_context(message)
    if ctx.valid:
        f = StringIO()
        with redirect_stdout(f):
            await bot.invoke(ctx)
            
        if f.getvalue():
            # Sending the output (all prints) to your channel.
            await ctx.send(f.getvalue())
        f.close()

        
bot.run(YOUR_SECRET_TOKEN)

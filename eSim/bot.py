# todo: more converters (k - 000 f.e)
# todo: default nick command.
import asyncio
from contextlib import redirect_stdout
from io import StringIO
from random import randint
from typing import Optional
from traceback import print_exception
from sys import stderr

import discord
from discord.ext import commands

import __init__  # For IDLE
from Basic import *
from Fight import *
from Help_functions.bot_functions import random_sleep
from Help_functions.login import get_content, get_nick_and_pw
from Time_saver import *

bot = commands.Bot(command_prefix=".", case_insensitive=True)
YOUR_SECRET_TOKEN = input("Your discord token (help - https://discordpy.readthedocs.io/en/latest/discord.html): ")
# YOUR_SECRET_TOKEN = "NEc3NTE1MDcwNHjkIoYzNjA2.X7EjVg.6dQHDfwIRSoWf31KCQwI9euGeeY"

# MY_NICKS = {"secura": "Some Nick",
#             "suna": "Another Nick"}

# If you have the same nick in all servers:
# MY_NICKS = defaultdict(lambda: "Your Nick")

MY_NICKS = get_nick_and_pw("all")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)


class IsMyNick(commands.Converter):
    async def convert(self, ctx, nick):
        if nick.lower() == MY_NICKS[ctx.channel.name].lower():
            return nick
        raise


def add_docs_for(other_func):
    def dec(func):
        if not other_func.__doc__:
            other_func.__doc__ = ""
        if not func.__doc__:
            func.__doc__ = ""
        func.__doc__ = other_func.__doc__ + "\n\n" + func.__doc__
        return func

    return dec


@bot.command(aliases=["w", "work+"])
async def work(ctx, *, nick: IsMyNick):
    """`work+` -> for premium users"""
    queue = "+" if ctx.invoked_with.lower() == "work+" else ""
    await login.double_click(ctx.channel.name, queue)


@bot.command()
@add_docs_for(accept_contract.accept_contract)
async def accept(ctx, contract_id, *, nick: IsMyNick):
    await accept_contract.accept_contract(ctx.channel.name, contract_id)


@bot.command()
@add_docs_for(battle_order.battle_order)
async def bo(ctx, battle_link, side, *, nick: IsMyNick):
    await battle_order.battle_order(ctx.channel.name, battle_link, side)


@bot.command()
@add_docs_for(bid.bid_specific_auction)
async def Bid(ctx, auction_id_or_link, price, delay, *, nick: IsMyNick):
    if delay.lower() not in ("yes", "no"):
        await ctx.send(f"delay parameter must to be 'yes' or 'no' (not {delay})")
        return
    else:
        delay = True if delay.lower() == "yes" else False
    await bid.bid_specific_auction(ctx.channel.name, auction_id_or_link, price, delay)


@bot.command(aliases=["Buffs"])
@add_docs_for(buff.buffs)
async def Buff(ctx, buffs_names, *, nick: IsMyNick):
    await buff.buffs(ctx.channel.name, buffs_names)


@bot.command()
@add_docs_for(buy_cc.cc)
async def cc(ctx, country_id, max_price, buy_amount, *, nick: IsMyNick):
    await buy_cc.cc(ctx.channel.name, country_id, max_price, buy_amount)


@bot.command()
@add_docs_for(buy_product.products)
async def buy(ctx, amount: int, quality: Optional[int] = 5, product="wep", *, nick: IsMyNick):
    await buy_product.products(ctx.channel.name, f'{quality} {product}', amount)


@bot.command()
@add_docs_for(candidate.candidate)
async def Candidate(ctx, *, nick: IsMyNick):
    await candidate.candidate(ctx.channel.name)


@bot.command()
@add_docs_for(change_avatar.avatar)
async def avatar(ctx, *, nick):
    """
    If you don't want the default img, write like that:
    `.avatar https://picsum.photos/150, Your Nick` (with a comma)"""
    if "," in nick:
        imgURL, nick = nick.split(",")
    else:
        imgURL = "https://source.unsplash.com/random/150x150"
    await IsMyNick().convert(ctx, nick)
    await change_avatar.avatar(ctx.channel.name, imgURL.strip())


@bot.command()
async def comment(ctx, shout_or_article_link, body, *, nick: IsMyNick):
    """
    - `body` parameter MUST be within quotes.
    - You can find shout link by clicking F12 in the page where you see the shout."""
    server = ctx.channel.name
    if "article" in shout_or_article_link:
        await comment_article.comment_article(server, shout_or_article_link.split("?id=")[1].split("&")[0], body)
    elif "shout" in shout_or_article_link:
        await comment_shout.comment_shout(server, shout_or_article_link.split("?id=")[1].split("&")[0], body)
    else:
        await ctx.send("Please provide a valid article/shout link.")


@bot.command()
@add_docs_for(donate_eqs.donate_eqs)
async def donate(ctx, ids, receiver_id: int, *, nick: IsMyNick):
    """`ids` MUST be separated by a comma, and without spaces (or with spaces, but within quotes)"""
    await donate_eqs.donate_eqs(ctx.channel.name, ids, str(receiver_id))


@bot.command(aliases=["Eqs"])
@add_docs_for(eqs.eqs)
async def eq(ctx, *, nick: IsMyNick):
    await eqs.eqs(ctx.channel.name)


@bot.command(aliases=["inv"])
@add_docs_for(inventory.Inventory)
async def muinv(ctx, *, nick: IsMyNick):
    products, quantity = await (inventory.Inventory if ctx.invoked_with.lower() == "inv" else mu_inventory.MU_Inventory)(
        ctx=True, server=ctx.channel.name)
    embed = discord.Embed(title=MY_NICKS[ctx.channel.name])
    for i in range(len(products) // 5 + 1):
        value = [f"**{a}**: {b}" for a, b in zip(products[i * 5:(i + 1) * 5], quantity[i * 5:(i + 1) * 5])]
        embed.add_field(name="**Products: **" if not i else u"\u200B", value="\n".join(value) if value else u"\u200B")
    embed.set_footer(text="Inventory" if ctx.invoked_with.lower() == "inv" else "Military Unit inventory")
    await ctx.send(embed=embed)


@bot.command()
@add_docs_for(fly.fly)
async def Fly(ctx, region_link_or_id, ticket_quality: Optional[int] = 5, *, nick: IsMyNick):
    """Default: Q5 tickets"""
    await fly.fly(ctx.channel.name, region_link_or_id, ticket_quality)


@bot.command()
@add_docs_for(job.job)
async def Job(ctx, *, nick: IsMyNick):
    await job.job(ctx.channel.name)


@bot.command(aliases=["dow", "mpp"])
@add_docs_for(mpp_dow_attack.mpp_dow_attack)
async def attack(ctx, ID: int, delay_or_battle_link, *, nick):
    """`delay_or_battle_link` - optional"""
    if not delay_or_battle_link.isdigit():
        nick = delay_or_battle_link + " " + nick
        delay_or_battle_link = ""
    await IsMyNick().convert(ctx, nick)
    await mpp_dow_attack.mpp_dow_attack(ctx.channel.name, str(ID), ctx.invoked_with.lower(), delay_or_battle_link)


@bot.command()
@add_docs_for(place_building.building)
async def build(ctx, regionId, quality, Round, *, nick: IsMyNick):
    """`quality` = building quality (if you want to build an hospital instead, write like that: `5-hospital`)"""
    await place_building.building(ctx.channel.name, regionId, quality, Round)


@bot.command()
@add_docs_for(read.read)
async def Read(ctx, *, nick: IsMyNick):
    await read.read(ctx.channel.name)


@bot.command()
@add_docs_for(register.register)
async def Register(ctx, nick: IsMyNick, lan, countryId):
    await register.register(ctx.channel.name, nick, get_nick_and_pw(ctx.channel.name)[1], lan, countryId)


@bot.command()
@add_docs_for(report_citizen.report)
async def report(ctx, target_id, report_reason, *, nick: IsMyNick):
    """`report_reason` MUST be within quotes"""
    await report_citizen.report(ctx.channel.name, target_id, report_reason)


@bot.command(aliases=["upgrade"])
@add_docs_for(reshuffle_or_upgrade.reshuffle_or_upgrade)
async def reshuffle(ctx, eq_id_or_link, parameter, *, nick: IsMyNick):
    """`parameter` - it's recommended to copy and paste, but you can also write first/last"""
    await reshuffle_or_upgrade.reshuffle_or_upgrade(ctx.channel.name, ctx.invoked_with.lower(), eq_id_or_link,
                                                    parameter)


@bot.command()
@add_docs_for(rw.rw)
async def RW(ctx, region_id_or_link, ticket_quality: Optional[int] = 5, *, nick: IsMyNick):
    await rw.rw(ctx.channel.name, region_id_or_link, ticket_quality)


@bot.command()
@add_docs_for(sell_eqs.sell_eqs)
async def sell(ctx, ids, price: float, hours: int, *, nick: IsMyNick):
    """`ids` MUST be separated by a comma, and without spaces (or with spaces, but within quotes)"""
    await sell_eqs.sell_eqs(ctx.channel.name, ids, price, hours)


@bot.command(aliases=["MU"])
@add_docs_for(send_application.citizenship_or_mu_application)
async def citizenship(ctx, country_or_mu_id: int, *, nick: IsMyNick):
    await send_application.citizenship_or_mu_application(ctx.channel.name, country_or_mu_id, ctx.invoked_with.lower())


@bot.command()
@add_docs_for(send_msg.send_msg)
async def msg(ctx, receiver_name, title, body, *, nick: IsMyNick):
    """If any arg (receiverName, title or body) containing more than 1 word - it must be within quotes"""
    await send_msg.send_msg(ctx.channel.name, receiver_name, title, body)


@bot.command()
@add_docs_for(shout.shout)
async def Shout(ctx, shout_body, *, nick: IsMyNick):
    """`shout_body` MUST be within quotes"""
    await shout.shout(ctx.channel.name, shout_body)


@bot.command(aliases=["vote", "Vote_shout"])
async def Sub(ctx, id: int, *, nick: IsMyNick):
    server = ctx.channel.name
    if ctx.invoked_with.lower() == "sub":
        await sub.sub(server, id)
    elif ctx.invoked_with.lower() == "vote":
        await vote_article.article(server, id)
    elif ctx.invoked_with.lower() == "vote_shout":
        await vote_shout.vote_shout(server, id)


@bot.command(aliases=["gift"])
@add_docs_for(use.use)
async def food(ctx, quality: Optional[int] = 5, *, nick: IsMyNick):
    """Default: Q5"""
    await use.use(ctx.channel.name, ctx.invoked_with.lower(), quality)


@bot.command()
@add_docs_for(vote_elections.elect)
async def elect(ctx, your_candidate, *, nick: IsMyNick):
    """If `your_candidate` containing more than 1 word - it must be within quotes"""
    await vote_elections.elect(ctx.channel.name, your_candidate)


@bot.command()
@add_docs_for(vote_law.law)
async def law(ctx, link_or_id, your_vote, *, nick: IsMyNick):
    await vote_law.law(ctx.channel.name, link_or_id, your_vote)


@bot.command(aliases=["unwear"])
async def wear(ctx, ids, *, nick: IsMyNick):
    """
    Wear/take off specific EQ IDs.
    `ids` MUST be separated by a comma, and without spaces (or with spaces, but within quotes)"""
    await wear_unwear.wear_unwear(ctx.channel.name, ids, "-" if ctx.invoked_with.lower() == "unwear" else "+")


@bot.command()
@add_docs_for(auto_fight.auto_fight)
async def add(ctx, nick: IsMyNick, restores: int = 100, battle_id: int = 0,
              side="attacker", wep: int = 0, food: int = 5, gift: int = 0):
    """
    If `nick` containing more than 1 word - it must be within quotes.
    If you want to skip a parameter, you should write the default value.
    Example: `.add "My Nick" 100 0 attacker 0 5` - write 0 to `battle_id` in order to change `food`"""
    # Idea: control all those parameters via google spreadsheets or something (read the data with python).
    if side.lower() not in ("attacker", "defender"):
        return await ctx.send(f"'side' parameter must be attacker/defender only (not {side})")
    await ctx.send("Ok sir!")
    await auto_fight.auto_fight(ctx.channel.name, battle_id, side, wep, food, gift, restores)


@bot.command()
@add_docs_for(fight.fight)
async def Fight(ctx, nick: IsMyNick, link, side, weaponQuality: int = 5,
                dmg_or_hits="100kk", ticketQuality: int = 5):
    """
    If `nick` containing more than 1 word - it must be within quotes.
    If you want to skip a parameter, you should write the default value.
        Example: `.fight "My Nick" 100 "" attacker 0 5` - skip `battle_id` in order to change `food`
    - You can't stop it after it started to fight, so be careful with `dmg_or_hits` parameter"""
    link = link if link.startswith("http") else f"https://{ctx.channel.name}.e-sim.org/battle.html?id={link}"
    await fight.fight(link, side, weaponQuality, dmg_or_hits, ticketQuality)


@bot.command()
@add_docs_for(hunt.hunt)
async def Hunt(ctx, nick: IsMyNick, maxDmgForBh="500k", weaponQuality: int = 5, startTime: int = 60):
    """If `nick` containing more than 1 word - it must be within quotes."""
    await hunt.hunt(ctx.channel.name, maxDmgForBh, str(startTime), weaponQuality)


@bot.command()
@add_docs_for(hunt_specific_battle.hunt_specific_battle)
async def hunt_battle(ctx, nick, link, side="attacker", max_dmg_for_bh: int = 1, weapon_quality: int = 0):
    """If `nick` containing more than 1 word - it must be within quotes."""
    link = link if link.startswith("http") else f"https://{ctx.channel.name}.e-sim.org/battle.html?id={link}"
    await hunt_specific_battle.hunt_specific_battle(link, side, str(max_dmg_for_bh), weapon_quality)


@bot.command(aliases=["Motivates"])
@add_docs_for(motivates.send_motivates)
async def motivate(ctx, *, nick):
    """
    If you want to send motivates with specific type only, write in this format:
    .motivate My Nick, wep"""
    if "," in nick:
        nick, Type = nick.split(",")
    else:
        Type = "all"
    await IsMyNick().convert(ctx, nick.strip())
    await motivates.send_motivates(ctx.channel.name, Type.strip())


@bot.command()
@add_docs_for(supply.supply)
async def Supply(ctx, amount: int, quality: Optional[int] = 5, product="wep", *, nick: IsMyNick):
    await supply.supply(ctx.channel.name, str(amount), f'{quality} {product}')


@bot.command()
@add_docs_for(watch.watch)
async def Watch(ctx, nick, link, side, start_time: int = 60,
                keep_wall="3kk", let_overkill="10kk", weaponQuality: int = 5):
    """If `nick` containing more than 1 word - it must be within quotes."""
    link = link if link.startswith("http") else f"https://{ctx.channel.name}.e-sim.org/battle.html?id={link}"
    await watch.watch(link, side, str(start_time), keep_wall, let_overkill, weaponQuality)


@bot.command(aliases=["friends+"])
@add_docs_for(add_friends.friends)
async def friends(ctx, *, nick: IsMyNick):
    await add_friends.friends(ctx.channel.name, "online" if ctx.invoked_with.lower() == "friends" else "all")


@bot.command()
async def medkit(ctx, *, nick: IsMyNick):
    post_use = await get_content(f"https://{ctx.channel.name}.e-sim.org/medkit.html", data={}, login_first=True)
    await ctx.send(post_use)


@bot.command()
async def merge(ctx, ids_or_Q, *, nick: IsMyNick):
    """
    Merge specific EQ IDs / all EQs up to specific Q (included).
    Examples:
    .merge 36191,34271,33877 My Nick
    .merge 5 My Nick
    IMPORTANT NOTE: No spaces in `ids_or_Q`! only commas.
    """
    await merge_storage.merge(ctx.channel.name, ids_or_Q)


@bot.command()
async def Missions(ctx, *, nick: IsMyNick):
    """Finish all missions."""
    await missions.missions(ctx.channel.name)


@bot.command()
@add_docs_for(sell_coins.mm)
async def mm(ctx, *, nick: IsMyNick):
    await sell_coins.mm(ctx.channel.name)


@bot.command()
@add_docs_for(login.login)
async def Login(ctx, *, nick: IsMyNick):
    """Should help you in error cases"""
    await login.login(ctx.channel.name, clear_cookies=True)


@bot.command()
async def shutdown(ctx, *, nick: IsMyNick):
    """Shutting down specific nick (in case of ban or something)
    Warning: It shutting down from all servers."""
    await ctx.send(f"**{nick}** shutted down")
    exit()


@bot.command()
async def limits(ctx, *, nick: IsMyNick):
    URL = f"https://{ctx.channel.name}.e-sim.org/"
    tree = await get_content(URL, login_first=True)
    gold = tree.xpath('//*[@id="userMenu"]//div//div[4]//div[1]/b/text()')[0]
    food_limit = tree.xpath('//*[@id="foodQ5"]/text()')[0]
    gift_limit = tree.xpath('//*[@id="giftQ5"]/text()')[0]
    food = int(float(tree.xpath('//*[@id="foodLimit2"]')[0].text))
    gift = int(float(tree.xpath('//*[@id="giftLimit2"]')[0].text))
    await ctx.send(f"Limits: {food}/{gift}. Storage: {food_limit}/{gift_limit}\n{gold} Gold.")


@bot.command(aliases=["last"], hidden=True)
async def ping(ctx, *, nicks):
    """Shows who is connected to host"""
    for nick in [x.strip() for x in nicks.split(",") if x.strip()]:
        if nick.lower() == "all":
            nick = MY_NICKS[ctx.server.name]
            await asyncio.sleep(randint(1, 3))

        if nick.lower() == MY_NICKS[ctx.server.name].lower():
            await ctx.send(f'**{MY_NICKS[ctx.server.name]}** - online')


@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    if ctx.valid:
        f = StringIO()
        with redirect_stdout(f):
            await bot.invoke(ctx)
        output = f.getvalue()

        if "notLoggedIn" in output or "error" in output:
            ctx = await bot.get_context(message)
            f = StringIO()
            with redirect_stdout(f):
                await bot.invoke(ctx)
            output = f.getvalue()

        if output:
            if len(output) > 100 or "http" in output:
                embed = discord.Embed(title=MY_NICKS[ctx.channel.name])
                for Index in range(len(output) // 1000 + 1)[:5]:
                    embed.add_field(name=f"Page {Index + 1}" if Index else u"\u200B", value=output[Index * 1000:(Index + 1) * 1000])
                # Sending the output (all prints) to your channel.
                await ctx.send(embed=embed)
            else:
                # Short msg.
                await ctx.send(output[:2000])
        f.truncate(0)
        f.seek(0)


@bot.event
async def on_command_error(ctx, error):
    error = getattr(error, 'original', error)
    if isinstance(error, RuntimeError):
        return
    if isinstance(error, commands.NoPrivateMessage):
        return await ctx.send("Sorry, you can't use this command in a private message!")
    if isinstance(error, commands.CommandNotFound):
        return
    print('Ignoring exception in command {}:'.format(ctx.command), file=stderr)
    print_exception(type(error), error, error.__traceback__, file=stderr)
    last_msg = str(list(await ctx.channel.history(limit=1).flatten())[0].content)
    error_msg = f'```{error}```'
    if error_msg != last_msg:
        # Don't send from all users.
        await ctx.send(error_msg)


bot.run(YOUR_SECRET_TOKEN)

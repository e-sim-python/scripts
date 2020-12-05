import discord
from discord.ext import commands
from io import StringIO
from contextlib import redirect_stdout
from collections import defaultdict

from Basic import *
from Fight import *
from Time_saver import *
from login import get_nick_and_pw


bot = commands.Bot(command_prefix=".", case_insensitive=True)
YOUR_SECRET_TOKEN = input("Your discord token (help - https://discordpy.readthedocs.io/en/latest/discord.html): ")

sessions = defaultdict(lambda: "")

# MY_NICKS = {"secura": "Some Nick",
#             "suna": "Another Nick"}

# If you have the same nick in all servers:
# MY_NICKS = defaultdict(lambda: "Your Nick")

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


@bot.command(aliases=["w", "work+"])
async def work(ctx, *, nick):
    """`work+` -> for premium users"""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        queue = "+" if ctx.invoked_with.lower() == "work+" else ""
        sessions[server] = login.double_click(server, queue, session)
        
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
        
@bot.command()
@add_docs_for(buy_cc.cc)
async def cc(ctx, country_id, max_price, buy_amount, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = buy_cc.cc(server, country_id, max_price, buy_amount, session)

@bot.command()
@add_docs_for(buy_product.products)
async def buy(ctx, product, amount, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = buy_product.products(server, product, amount, session)

@bot.command()
@add_docs_for(candidate.candidate)
async def candidate(ctx, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = candidate.candidate(server, session)

@bot.command()
@add_docs_for(change_avatar.avatar)
async def avatar(ctx, *, nick):
    """
    If you don't want the default img, write like that:
    `.avatar https://picsum.photos/150, Your Nick` (with a comma)"""
    server = ctx.channel.name
    if "," in nick:
        imgURL, nick = nick.split(",")
    else:
        imgURL = "https://source.unsplash.com/random"
    if nick.strip().lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = change_avatar.avatar(server, imgURL.strip(), session)

@bot.command()
async def comment(ctx, shout_or_article_link, body, *, nick):
    """
    - `body` parameter MUST be within quotes.
    - You can find shout link by clicking F12 in the page where you see the shout."""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        if "article" in shout_or_article_link:
            sessions[server] = comment_article.comment_article(server, shout_or_article_link.split("?id=")[1].split("&")[0], body, session)
        elif "shout" in shout_or_article_link:
            sessions[server] = comment_shout.comment_shout(server, shout_or_article_link.split("?id=")[1].split("&")[0], body, session)
        else:
            await ctx.send("Please provide a valid article/shout link.")

@bot.command()
@add_docs_for(donate_eqs.donate_eqs)
async def donate(ctx, ids, receiver_id, *, nick):
    """`ids` MUST be separated by a comma, and without spaces (or with spaces, but within quotes)"""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = donate_eqs.donate_eqs(server, ids, receiver_id, session)

@bot.command()
@add_docs_for(eqs.eqs)
async def eq(ctx, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = eqs.eqs(server, session)
        # to do: aliases=["storage", "inventory"] (show all storage).

@bot.command()
@add_docs_for(fly.fly)
async def Fly(ctx, region_link_or_id, ticket_quality, *, nick):
    """Default: Q5 tickets"""
    server = ctx.channel.name
    try:
        int(ticket_quality)
    except:
        nick = ticket_quality + " " + nick
        ticket_quality = 5
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = fly.fly(server, region_link_or_id, ticket_quality, session)

@bot.command()
@add_docs_for(job.job)
async def Job(ctx, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = job.job(server, session)

@bot.command(aliases=["dow", "mpp"])
@add_docs_for(mpp_dow_attack.mpp_dow_attack)
async def attack(ctx, ID, delay_or_battle_link, *, nick):
    """`delay_or_battle_link` - optional"""
    server = ctx.channel.name
    if ".e-sim.org/battle.html?id=" not in delay_or_battle_link:
        try:
            int(delay_or_battle_link)
        except:
            nick = delay_or_battle_link + " " + nick
            delay_or_battle_link = ""
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = mpp_dow_attack.mpp_dow_attack(server, ID, ctx.invoked_with.lower(), delay_or_battle_link, session)

@bot.command()
@add_docs_for(place_building.building)
async def build(ctx, regionId, quality, Round, *, nick):
    """`quality` = building quality (if you want to build an hospital instead, write like that: `5-hospital`)"""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = place_building.building(server, regionId, quality, Round, session)

@bot.command()
@add_docs_for(read.read)
async def Read(ctx, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = read.read(server, session)

@bot.command()
@add_docs_for(register.register)
async def Register(ctx, lan, countryId, password, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = register.register(server, nick, password, lan, countryId, session)

@bot.command()
@add_docs_for(report_citizen.report)
async def report(ctx, target_id, report_reason, *, nick):
    """`report_reason` MUST be within quotes"""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = report_citizen.report(server, target_id, report_reason, session)

@bot.command(aliases=["upgrade"])
@add_docs_for(reshuffle_or_upgrade.reshuffle_or_upgrade)
async def reshuffle(ctx, eq_id_or_link, parameter, *, nick):
    """`parameter` - it's recommended to copy and paste, but you can also write first/last"""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = reshuffle_or_upgrade.reshuffle_or_upgrade(server, ctx.invoked_with.lower(), eq_id_or_link, parameter, session)

@bot.command()
@add_docs_for(rw.rw)
async def RW(ctx, region_id_or_link, ticket_quality, *, nick):
    server = ctx.channel.name
    try:
        int(ticket_quality)
    except:
        nick = ticket_quality + " " + nick
        ticket_quality = 5
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = rw.rw(server, region_id_or_link, ticket_quality, session)

@bot.command()
@add_docs_for(sell_eqs.sell_eqs)
async def sell(ctx, ids, price, hours, *, nick):
    """`ids` MUST be separated by a comma, and without spaces (or with spaces, but within quotes)"""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = sell_eqs.sell_eqs(server, ids, price, hours, session)

@bot.command(aliases=["MU"])
@add_docs_for(send_application.citizenship_or_mu_application)
async def citizenship(ctx, country_or_mu_id, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = send_application.citizenship_or_mu_application(server, country_or_mu_id, ctx.invoked_with.lower(), session)

@bot.command()
@add_docs_for(send_msg.send_msg)
async def msg(ctx, receiver_name, title, body, *, nick):
    """If any arg (receiverName, title or body) containing more than 1 word - it must be within quotes"""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = send_msg.send_msg(server, receiver_name, title, body, session)

@bot.command()
@add_docs_for(shout.shout)
async def Shout(ctx, shout_body, *, nick):
    """`shout_body` MUST be within quotes"""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = shout.shout(server, shout_body, session)

@bot.command(aliases=["vote", "Vote_shout"])
async def Sub(ctx, id, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        if ctx.invoked_with.lower() == "sub":
            sessions[server] = sub.sub(server, id, session)
        elif ctx.invoked_with.lower() == "vote":
            sessions[server] = vote_article.article(server, id, session)
        elif ctx.invoked_with.lower() == "vote_shout":
            sessions[server] = vote_shout.vote_shout(server, id, session)

@bot.command(aliases=["gift"])
@add_docs_for(use.use)
async def food(ctx, quality, *, nick):
    """Default: Q5"""
    server = ctx.channel.name
    try:
        int(quality)
    except:
        nick = quality + " " + nick
        quality = 5
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = use.use(server, ctx.invoked_with.lower(), quality, session)

@bot.command()
@add_docs_for(vote_elections.elect)
async def elect(ctx, your_candidate, *, nick):
    """If `your_candidate` containing more than 1 word - it must be within quotes"""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = vote_elections.elect(server, your_candidate, session)

@bot.command()
@add_docs_for(vote_law.law)
async def law(ctx, link_or_id, your_vote, *, nick):    
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = vote_law.law(server, link_or_id, your_vote, session)

@bot.command(aliases=["unwear"])
async def wear(ctx, ids, *, nick):
    """
    Wear/take off specific EQ IDs.
    `ids` MUST be separated by a comma, and without spaces (or with spaces, but within quotes)"""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        action = "-" if ctx.invoked_with.lower() == "unwear" else "+"
        sessions[server] = wear_unwear.wear_unwear(server, ids, action, session)

@bot.command()
@add_docs_for(auto_fight.auto_fight)
async def add(ctx, nick, restores="100", battle_id="", side="attacker", wep="0", food="", gift=""):
    """
    If `nick` containing more than 1 word - it must be within quotes.
    If you want to skip a parameter, you should write the default value.
    Example: `.add "My Nick" 100 "" attacker 0 5` - skip `battle_id` in order to change `food`"""
    # Idea: control all those parameters via google spreadsheets or something (read the data with python).
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        if side.lower() not in ("attacker", "defender"):
            await ctx.send(f"'side' parameter must be attacker/defender only (not {side})")
        auto_fight.auto_fight(server, battle_id, side, wep, food, gift, restores)

@bot.command()
@add_docs_for(fight.fight)
async def Fight(ctx, nick, link, side, weaponQuality="5", dmg_or_hits="100kk", ticketQuality="5"):
    """
    If `nick` containing more than 1 word - it must be within quotes.
    If you want to skip a parameter, you should write the default value.
    Example: `.fight "My Nick" 100 "" attacker 0 5` - skip `battle_id` in order to change `food`"""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        link = link if link.startswith("http") else f"https://{server}.e-sim.org/battle.html?id={link}"
        session = sessions[server]
        sessions[server] = fight.fight(link, side, weaponQuality, dmg_or_hits, ticketQuality, session)

@bot.command()
@add_docs_for(hunt.hunt)
async def Hunt(ctx, nick, maxDmgForBh="500000", weaponQuality="5", startTime="60"):
    """If `nick` containing more than 1 word - it must be within quotes."""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        hunt.hunt(server, maxDmgForBh, startTime, weaponQuality)

@bot.command()
@add_docs_for(hunt_specific_battle.hunt_specific_battle)
async def hunt_battle(ctx, nick, link, side="attacker", max_dmg_for_bh="1", weapon_quality="0"):
    """If `nick` containing more than 1 word - it must be within quotes."""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        link = link if link.startswith("http") else f"https://{server}.e-sim.org/battle.html?id={link}"
        hunt_specific_battle.hunt_specific_battle(link, side, max_dmg_for_bh, weapon_quality)

@bot.command()
@add_docs_for(motivates.send_motivates)
async def motivate(ctx, *, nick):
    """
    If you want to send motivates with specific type only, write in this format:
    .motivate My Nick, wep"""
    if "," in nick:
        nick, Type = nick.split(",")
    else:
        Type = "all"
    server = ctx.channel.name
    if nick.strip().lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = motivates.send_motivates(server, Type.strip(), session)

@bot.command()
@add_docs_for(supply.supply)
async def Supply(ctx, amount, quality, product, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        product = f'{int(quality.lower().replace("Q", ""))} {product}'
        session = sessions[server]
        sessions[server] = supply.supply(server, amount, product, session)

@bot.command()
@add_docs_for(win_battle.watch)
async def watch(ctx, nick, link, side, start_time="60", keep_wall="3kk", let_overkill="10000000", weaponQuality="5"):
    """If `nick` containing more than 1 word - it must be within quotes."""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        link = link if link.startswith("http") else f"https://{server}.e-sim.org/battle.html?id={link}"
        win_battle.watch(link, side, start_time, keep_wall, let_overkill, weaponQuality)

@bot.command(aliases=["friends+"])
@add_docs_for(add_friends.friends)
async def friends(ctx, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        option = "online" if ctx.invoked_with.lower() == "friends" else "all"
        session = sessions[server]
        sessions[server] = add_friends.friends(server, option, session)

@bot.command()
async def merge(ctx, ids_or_Q, *, nick):
    """
    Merge specific EQ IDs / all EQs up to specific Q (included).
    Examples:
    .merge 36191,34271,33877 My Nick
    .merge 5 My Nick
    IMPORTANT NOTE: No spaces in `ids_or_Q`! only commas.
    """
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = merge_storage.merge(server, ids_or_Q, session)

@bot.command()
async def Missions(ctx, *, nick):
    """Finish all missions."""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        missions.missions(server, session=session)

@bot.command()
@add_docs_for(sell_coins.mm)
async def mm(ctx, *, nick):
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        session = sessions[server]
        sessions[server] = sell_coins.mm(server, session)

@bot.command()
@add_docs_for(login.login)
async def Login(ctx, *, nick):
    """Should help you in error cases"""
    server = ctx.channel.name
    if nick.lower() == MY_NICKS[server].lower():
        sessions[server] = login.login(server)

@bot.command()
async def shutdown(ctx, *, nick):
    """Shuting down specific nick (in case of ban or something)
    Warning: It shuting down from all servers."""
    if nick.lower() == MY_NICKS[server].lower():
        await ctx.send(f"**{nick}** shutted down")
        sys.exit(1)
        
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
            sessions[ctx.channel.name] = login.login(ctx.channel.name)
            with redirect_stdout(f):
                await bot.invoke(ctx)
            output = f.getvalue()
            
        if output:
            if len(output) > 100 or "http" in output:
                embed = discord.Embed()
                embed.add_field(name=MY_NICKS[ctx.channel.name].lower(), value=output[:1000])
                if output[1000:]:
                    embed.add_field(name="Page 2", value=output[1000:2000])
                # Sending the output (all prints) to your channel.
                await ctx.send(embed=embed)
            else:
                await ctx.send(output[:2000])
        f.close()

@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return
    error = getattr(error, 'original', error)
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send("Sorry, you can't use this command in a private message!")
        return
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(error,delete_after=5)
        return
    last_msg = str(list(await ctx.channel.history(limit=1).flatten())[0].content)
    error_msg = f'```{error}```'
    if error_msg != last_msg:
        # Don't send from all users.
        await ctx.send(error_msg)
        
bot.run(YOUR_SECRET_TOKEN)

import asyncio
import csv
import os
from datetime import datetime
from random import choice, randint

from Time_saver.utils import fight395791_
from login import get_content, get_nick_and_pw


def fix_product_name(product):
    item = product.split()
    options = "iron, grain, oil, stone, wood, diamonds (diam), weapon (wep), house, gift, food, ticket, defense_system (DS), hospital, estate"
    Q = item[0].replace("Q", "").replace("q", "") if len(item) == 2 else None
    item = item[1].upper() if len(item) == 2 else item[0].upper()
    if item in ("DS", "DEFENSE SYSTEM"):
        item = "DEFENSE_SYSTEM"
    if item.endswith("S"):
        item = item[:-1]
    if item in ("DIAMOND", "DIAM"):
        item = "DIAMONDS"
    elif item in ("WEP", "WEAP"):
        item = "WEAPON"

    if item not in options.upper():
        print(f'"product" parameter must be one of those: {options}.\n(not {product})')
        return False, False
    else:
        return Q, item


async def get_staff_list(URL):
    blacklist = set()
    tree = await get_content(f"{URL}staff.html", login_first=True)
    nicks = tree.xpath('//*[@id="esim-layout"]//a/text()')
    for nick in nicks:
        blacklist.add(nick.strip())
    return blacklist


async def get_battle_id(server, battle_id):
    URL = f"https://{server}.e-sim.org/"
    nick = get_nick_and_pw(server)[0]
    apiCitizen = await get_content(f"{URL}apiCitizenByName.html?name={nick.lower()}")
    for row in await get_content(f'{URL}apiMap.html'):
        if row['regionId'] == apiCitizen['currentLocationRegionId']:
            occupantId = row['occupantId']
            break
    try:
        if apiCitizen["level"] < 15:
            raise  # PRACTICE_BATTLE
        if battle_id == "event":
            tree = await get_content(f"{URL}battles.html?countryId={apiCitizen['citizenshipId']}&filter=EVENT")
            for link in tree.xpath("//tr[position()<12]//td[1]//div[2]//a/@href"):
                link_id = link.split('=')[1]
                apiBattles = await get_content(f"{URL}apiBattles.html?battleId={link_id}")
                if apiCitizen['citizenshipId'] in (apiBattles['attackerId'], apiBattles['defenderId']):
                    battle_id = link_id
                    break

        else:
            tree = await get_content(f"{URL}battles.html?countryId={occupantId}&filter=NORMAL")
            battle_id = tree.xpath('//tr//td[1]//div//div[2]//div[2]/a/@href')
        if not battle_id:
            tree = await get_content(f"{URL}battles.html?countryId={occupantId}&filter=RESISTANCE")
            battle_id = tree.xpath('//tr//td[1]//div//div[2]//div[2]/a/@href')
    except:
        tree = await get_content(f"{URL}battles.html?filter=PRACTICE_BATTLE")
        battle_id = tree.xpath('//tr[2]//td[1]//a/@href')
    battle_id = battle_id[0].replace("battle.html?id=", "") or None
    return battle_id


async def random_sleep(restores_left="100"):
    # Functions: datetime (datetime), randint (random), time
    if restores_left:
        now = datetime.now()
        minutes = int(now.strftime("%M"))
        sec = int(now.strftime("%S"))
        roundup = round(minutes + 5.1, -1)  # round up to the next ten minutes (00:10, 00:20 etc)
        random_number = randint(30, 570)  # getting random number
        sleep_time = random_number + (roundup - minutes) * 60 - sec
        print(f"Sleeping for {sleep_time} seconds.")
        await asyncio.sleep(sleep_time)


async def special_items_list(server):
    # Not in use.
    # Functions: login, fromstring
    tree = await get_content(f"https://{server}.e-sim.org/storage.html?storageType=SPECIAL_ITEM")
    storage = []
    for num in range(1, 16):
        try:
            amount = tree.xpath(f'//*[@id="storageConteiner"]//div//div//div[1]//div[{num}]/span')[0].text
            if "x" in amount:
                item = str(tree.xpath(f'//*[@id="storageConteiner"]//div//div//div[1]//div[{num}]/b')[0].text)
                item = item.replace("Extra", "").replace("Equipment parameter ", "")
                if item != "Medkit" and "Bandage" not in item:
                    storage.append(f'{amount.replace("x", "")} {item}')
        except:
            break

    print(", ".join(storage))


slots = ['Helmet', 'Vision', 'Personal Armor', 'Pants',
         'Shoes', 'Lucky charm', 'Weapon upgrade', 'Offhand']


async def create_auctions_csv(file_name):
    with open(file_name, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["Item"] + [f"Q{q}" for q in range(1, 8)])
        for slot in slots:
            writer.writerow([slot])


async def auctions_csv_helper(file_name):
    with open(file_name, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["Item"] + [f"Q{q}" for q in range(1, 8)])
        for slot in slots:
            row = [slot]
            for q in range(1, 8):
                user_price = input(f"Pls write price for Q{q} {slot} (remember the hints above): ")
                row.append(user_price)
            writer.writerow(row)


async def update_auctions_prices_from_csv(prices, file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] in prices:
                for Index, column in enumerate(row):
                    if Index != 0:
                        prices[row[0]][f"Q{Index}"] = column
    return prices


async def converting_raw_price_to_float(price):
    if not price or price == "0":
        price = 0
    elif "-" in price:
        price = float(choice(price.split("-")))
    elif "," in price:
        price = float("{0:.2f}".format(price.split(",")))
    else:
        price = float(price)
    return price


async def prices_helper(file_name):
    if not os.path.isfile(file_name):
        await create_auctions_csv(file_name)
        print(
            f"I have created a new excel file in the script folder, called {file_name}. "
            "You will have to fill it out (at least partially) alone or with my help.\n"
            "Notes: separate the prices with a hyphen (-) if you want "
            "the bot to choose randomly between those specific prices")
        print("Separate the prices with a comma (,) if you want the bot to pick random number from those numbers range")
        print("If you don't want to bid on specific type, leave it black or write 0")
        Help = input(
            "If you want to fill it alone, do it, save the file (as csv!), and then press Enter. otherwise, click 1: ")
        if Help == "1":
            await auctions_csv_helper(file_name)


def convert_to_dict(s):
    s_list = s.split("&")
    s_list[0] = f"ip={s_list[0]}"
    return dict([a.split("=") for a in s_list])


async def fighting(server, battle_id, side, wep):
    URL = f"https://{server}.e-sim.org/"

    for x in range(20):  # hitting until you have 0 health.
        try:
            tree = await get_content(f'{URL}battle.html?id={battle_id}')
            Health = int(float(tree.xpath('//*[@id="actualHealth"]')[0].text))
            if not Health:
                break
            value = "Berserk" if Health >= 50 else ""
            await send_fight_request(URL, tree, wep, side, value)
            print(f"Hit {x}")
            await asyncio.sleep(randint(1, 2))
        except Exception as e:
            print(e)
            await asyncio.sleep(randint(2, 5))


async def send_fight_request(URL, tree, wep, side, value="Berserk"):
    hidden_id = tree.xpath("//*[@id='battleRoundId']")[0].value
    fight395791 = fight395791_(tree.text_content())
    data = {"weaponQuality": wep, "battleRoundId": hidden_id, "side": side, "value": value}
    data.update(convert_to_dict("".join(tree.xpath("//script[3]/text()")).split("&ip=")[1].split("'")[0]))
    return await get_content(f"{URL}{fight395791}", data=data)


async def location(server):
    """getting current location"""
    URL = f"https://{server}.e-sim.org/"
    nick = get_nick_and_pw(server)[0]
    await asyncio.sleep(randint(1, 2))
    apiCitizen = await get_content(f"{URL}apiCitizenByName.html?name={nick.lower()}")
    return apiCitizen['currentLocationRegionId']

import csv
import os
import time
from datetime import datetime
from random import randint, choice

import requests
from lxml.html import fromstring

from login import login, get_nick_and_pw
import __init__
from Time_saver.utils import fight395791_


def _fix_product_name(product):
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


def _get_staff_list(URL):
    blacklist = set()
    i = requests.get(f"{URL}staff.html", verify=False)
    tree = fromstring(i.content)
    nicks = tree.xpath('//*[@id="esim-layout"]//a/text()')
    for nick in nicks:
        blacklist.add(nick.strip())
    return blacklist


def _get_battle_id(server, battle_id, session):
    URL = f"https://{server}.e-sim.org/"
    nick = get_nick_and_pw(server)[0]
    apiCitizen = session.get(f"{URL}apiCitizenByName.html?name={nick.lower()}").json()
    currentLocationRegionId = apiCitizen['currentLocationRegionId']
    apiMap = session.get(f'{URL}apiMap.html').json()
    for row in apiMap:
        if row['regionId'] == currentLocationRegionId:
            occupantId = row['occupantId']
            break
    try:
        if apiCitizen["level"] < 15:
            int("a")  # PRACTICE_BATTLE
        if battle_id == "event":
            battles = session.get(f"{URL}battles.html?countryId={apiCitizen['citizenshipId']}&filter=EVENT")
            tree = fromstring(battles.content)
            links = tree.xpath("//tr[position()<12]//td[1]//div[2]//@href")
            for link in links:
                link_id = link.split('=', 1)[1]
                apiBattles = session.get(f"{URL}apiBattles.html?battleId={link_id}").json()[0]
                if apiCitizen['citizenshipId'] in (apiBattles['attackerId'], apiBattles['defenderId']):
                    battle_id = link_id
                    break

        else:
            battles = session.get(f"{URL}battles.html?countryId={occupantId}&filter=NORMAL")
            tree = fromstring(battles.content)
            battle_id = tree.xpath('//tr[2]//td[1]//div[2]//@href')
        if not battle_id:
            battles = session.get(f"{URL}battles.html?countryId={occupantId}&filter=RESISTANCE")
            tree = fromstring(battles.content)
            battle_id = tree.xpath('//tr[2]//td[1]//div[2]//@href')
    except:
        battles = session.get(f"{URL}battles.html?filter=PRACTICE_BATTLE")
        tree = fromstring(battles.content)
        battle_id = tree.xpath('//tr[2]//td[1]//@href')
    battle_id = battle_id[0].replace("battle.html?id=", "") or None
    return battle_id


def _random_sleep(restores_left="100"):
    # Functions: datetime (datetime), randint (random), time
    if restores_left:
        now = datetime.now()
        minutes = int(now.strftime("%M"))
        sec = int(now.strftime("%S"))
        roundup = round(minutes + 5.1, -1)  # round up to the next ten minutes (00:10, 00:20 etc)
        random_number = randint(30, 570)  # getting random number
        sleep_time = random_number + (roundup - minutes) * 60 - sec
        print(f"Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)


def _special_items_list(server, session=""):
    # unfinished (&not in use)
    # Functions: login, fromstring
    """medkits = ""                  
    for letter in str(tree.xpath('//*[@id="medkitButton"]')[0].text):
        if letter in "1234567890": medkits = medkits+letter
i = session.get(url+'storage.html?storageType=SPECIAL_ITEM')
tree = html.fromstring(i.content)
storage = []
for num in range(1,16):
    try:
        ammount = tree.xpath(f'//*[@id="storageConteiner"]//div//div//div[1]//div[{num}]/span')[0].text
        if "x" in ammount:item = tree.xpath(f'//*[@id="storageConteiner"]//div//div//div[1]//div[{num}]/b')[0].text
        if item != "Medkit":storage.append(f'{ammount.replace("x","")} {item}')    
    except:break
i = session.get(url+'storage.html?storageType=PRODUCT')
tree = html.fromstring(i.content)
storage1 = {}
for num in range(2,22):
    try:
        item = str(tree.xpath(f'//*[@id="resourceInput"]/option[{num}]')[0].text).strip().replace("(available","").replace(")","").split(":")
        while "  " in item[0]: item[0] = item[0].replace("  ","")

        storage1[item[0]] = int(item[1])
    except:break
print(", ".join(storage))
print(", ".join([f'{v} {k}' for k,v in storage1.items()]))
        """
    if not session:
        session = login(server)
    special_items_page = session.get(f"https://{server}.e-sim.org/storage.html?storageType=SPECIAL_ITEM")
    tree = fromstring(special_items_page.content)
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


def _create_auctions_csv(file_name):
    with open(file_name, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["Item"] + [f"Q{q}" for q in range(1, 8)])
        for slot in slots:
            writer.writerow([slot])


def _auctions_csv_helper(file_name):
    with open(file_name, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["Item"] + [f"Q{q}" for q in range(1, 8)])
        for slot in slots:
            row = [slot]
            for q in range(1, 8):
                user_price = input(f"Pls write price for Q{q} {slot} (remember the hints above): ")
                row.append(user_price)
            writer.writerow(row)


def _update_auctions_prices_from_csv(prices, file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] in prices:
                for Index, column in enumerate(row):
                    if Index != 0:
                        prices[row[0]][f"Q{Index}"] = column
    return prices


def _converting_raw_price_to_float(price):
    if not price or price == "0":
        price = 0
    elif "-" in price:
        price = float(choice(price.split("-")))
    elif "," in price:
        price = float("{0:.2f}".format(price.split(",")))
    else:
        price = float(price)
    return price


def _prices_helper(file_name):
    if not os.path.isfile(file_name):
        _create_auctions_csv(file_name)
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
            _auctions_csv_helper(file_name)


def convert_to_dict(s):
    s_list = s.replace("'", '').split("&")
    s_list[0] = f"ip={s_list[0]}"
    return dict([a.split("=") for a in s_list])


def _fighting(server, battle_id, side, wep, session=""):
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    for _ in range(20):  # hitting until you have 0 health.
        try:
            battle_request = session.get(f'{URL}battle.html?id={battle_id}')
            tree = fromstring(battle_request.content)
            Health = int(float(tree.xpath('//*[@id="actualHealth"]')[0].text))
            if not Health:
                break
            if Health >= 50:
                value = "Berserk"
            else:
                value = ""
            HIT = send_fight_request(session, URL, tree, wep, side, value)
            print(HIT.url)
            time.sleep(randint(1, 2))
        except Exception as e:
            print(e)
            time.sleep(randint(2, 5))


def send_fight_request(session, URL, tree, wep, side, value="Berserk"):
    hidden_id = tree.xpath("//*[@id='battleRoundId']")[0].value
    fight395791 = fight395791_(tree.text_content())
    data = {"weaponQuality": wep, "battleRoundId": hidden_id, "side": side, "value": value}
    data.update(convert_to_dict("".join(tree.xpath("//script[3]/text()")).split("&ip=")[1].split(";")[0]))
    return session.post(f"{URL}{fight395791}", data=data)


def _location(server):
    """getting current location"""
    URL = f"https://{server}.e-sim.org/"
    nick = get_nick_and_pw(server)[0]
    time.sleep(randint(1, 2))
    apiCitizen = requests.get(f"{URL}apiCitizenByName.html?name={nick.lower()}", verify=False).json()
    currentLocationRegionId = apiCitizen['currentLocationRegionId']
    return currentLocationRegionId

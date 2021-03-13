from login import login
import __init__
from Basic.fly import fly
from Help_functions._bot_functions import send_fight_request

import requests
from lxml.html import fromstring
import time


def fight(link, side, weaponQuality="0", dmg_or_hits="100kk", ticketQuality="5", session=""):
    """
    Dumping limits in specific battle.
    * It will auto fly to bonus region.
    * dmg_or_hits < 1000 it's hits, otherwise - dmg."""
    server = link.replace("http://", "https://").split("https://", 1)[1].split(".e-sim.org", 1)[0]
    URL = f"https://{server}.e-sim.org/"
    side = side.lower()
    if side not in ("defender", "attacker"):
        print(f'side must be "defender" or "attacker" (not {side})')
        return
    dmg = int(dmg_or_hits.replace("k", "000"))
    api = requests.get(link.replace("battle", "apiBattles").replace("id", "battleId")).json()[0]
    if not session:
        session = login(server)
    r = session.get(link)
    print(r.url)
    main_tree = fromstring(r.content)
    food_limit = main_tree.xpath('//*[@id="sfoodQ5"]/text()')[0]
    gift_limit = main_tree.xpath('//*[@id="sgiftQ5"]/text()')[0]
    food = int(float(main_tree.xpath('//*[@id="foodLimit2"]')[0].text))
    gift = int(float(main_tree.xpath('//*[@id="giftLimit2"]')[0].text))
    if weaponQuality != "0":
        wep = main_tree.xpath(f'//*[@id="Q{weaponQuality}WeaponStock"]/text()')[0]
    else:
        wep = "unlimited"

    if api['type'] == "ATTACK":
        if side.lower() == "attacker":
            apiMap = requests.get(f'{URL}apiMap.html').json()
            apiRegions = requests.get(f'{URL}apiRegions.html').json()
            try:
                neighboursId = [region['neighbours'] for region in apiRegions if region["id"] == api['regionId']][0]
                aBonus = [i for region in apiMap for i in neighboursId if
                          i == region['regionId'] and region['occupantId'] == api['attackerId']]
            except:
                aBonus = [api['attackerId'] * 6]
            fly(server, aBonus[0], ticketQuality, session)
        elif side.lower() == "defender":
            fly(server, api['regionId'], ticketQuality, session)
    elif api['type'] == "RESISTANCE":
        fly(server, api['regionId'], ticketQuality, session)
    print(f"Limits: {food}/{gift}. Storage: {food_limit}/{gift_limit}/{wep} Q{weaponQuality} weps.")
    DamageDone = 0
    start_time = api["hoursRemaining"] * 3600 + api["minutesRemaining"] * 60 + api["secondsRemaining"]
    start = time.time()
    update = 1
    Damage = 0
    Health = int(float(main_tree.xpath('//*[@id="actualHealth"]')[0].text))
    while 1:
        if time.time() - start > int(start_time):
            break  # round is over        

        if Health < 50:
            if (not food or not int(food_limit)) and (not gift or not int(gift_limit)):
                print("done limits")
                break
            if gift and int(gift_limit):
                # use gifts limits first (save motivates limits)
                use = "gift"
                gift -= 1
            elif not food or not int(food_limit):
                use = "gift"
                gift -= 1
            else:
                use = "eat"
                food -= 1
            session.post(f"{URL}{use}.html", data={'quality': 5})
        for _ in range(5):
            try:
                post_hit = send_fight_request(session, URL, main_tree, weaponQuality, side)
                tree = fromstring(post_hit.content)
                Damage = int(str(tree.xpath('//*[@id="DamageDone"]')[0].text).replace(",", ""))
                Health = float(tree.xpath("//*[@id='healthUpdate']")[0].text.split()[0])
                if dmg < 1000:
                    Damage = 5  # Berserk
                update += 1
                break
            except:
                # "Slow down"
                delete = tree.xpath('//img/@src')
                if delete and "delete.png" in delete[0]:
                    break
                print("Slow down")
                time.sleep(2)
        DamageDone += Damage
        hits_or_dmg = "hits" if dmg < 1000 else "dmg"
        if update % 4 == 0:
            # dmg update every 4 berserks.
            print(f"{hits_or_dmg.title()} done so far: {DamageDone}")
        if DamageDone >= dmg:
            print(f"Done {DamageDone} {hits_or_dmg}")
            break
        if not food and not gift and not Health:
            use_medkit = input(f"Done limits. use medkit and continue (y/n)?")
            if use_medkit == "y":
                session.post(f"{URL}medkit.html")
            else:
                break
        time.sleep(1)
    return session


if __name__ == "__main__":
    print(fight.__doc__)
    link = input("battle link: ")
    side = input("Side (attacker/defender): ")
    if side.lower() not in ("attacker", "defender"):
        print(f"'side' parameter must be attacker/defender only (not {side})")
        raise SystemExit()
    weapon_quality = input("Weapon quality (0-5): ")
    dmg_or_hits = input("If you want to hit certain dmg/hits, write the amount: ")
    if not dmg_or_hits:
        dmg_or_hits = "100kk"
    ticketQuality = input("Ticket quality (1-5): ")
    fight(link, side, weapon_quality, dmg_or_hits, ticketQuality)
    input("Press any key to continue")

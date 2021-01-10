import asyncio
import time

import __init__  # For IDLE
from Basic.fly import fly
from login import get_content


async def fight(link, side, weaponQuality="0", dmg_or_hits="100kk", ticketQuality="5"):
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
    api = await get_content(link.replace("battle", "apiBattles").replace("id", "battleId"))

    tree = await get_content(link, login_first=True)
    food_limit = tree.xpath('//*[@id="sfoodQ5"]/text()')[0]
    gift_limit = tree.xpath('//*[@id="sgiftQ5"]/text()')[0]
    food = int(float(tree.xpath('//*[@id="foodLimit2"]')[0].text))
    gift = int(float(tree.xpath('//*[@id="giftLimit2"]')[0].text))
    if int(weaponQuality):
        wep = tree.xpath(f'//*[@id="Q{weaponQuality}WeaponStock"]/text()')[0]
    else:
        wep = "unlimited"

    if api['type'] == "ATTACK":
        if side.lower() == "attacker":
            try:
                neighboursId = [region['neighbours'] for region in await get_content(f'{URL}apiRegions.html') if region["id"] == api['regionId']][0]
                aBonus = [i for region in await get_content(f'{URL}apiMap.html') for i in neighboursId if
                          i == region['regionId'] and region['occupantId'] == api['attackerId']]
            except:
                aBonus = [api['attackerId'] * 6]
            await fly(server, aBonus[0], ticketQuality)
        elif side.lower() == "defender":
            await fly(server, api['regionId'], ticketQuality)
    elif api['type'] == "RESISTANCE":
        await fly(server, api['regionId'], ticketQuality)
    print(f"Limits: {food}/{gift}. Storage: {food_limit}/{gift_limit}/{wep} Q{weaponQuality} weps.")
    DamageDone = 0
    start_time = api["hoursRemaining"] * 3600 + api["minutesRemaining"] * 60 + api["secondsRemaining"]
    start = time.time()
    update = 0
    Damage = 0
    hidden_id = tree.xpath("//*[@id='battleRoundId']")[0].value
    for _ in range(100):
        if time.time() - start > int(start_time):
            break  # round is over
        tree = await get_content(link)
        Health = int(float(tree.xpath('//*[@id="actualHealth"]')[0].text))
        food_limit = tree.xpath('//*[@id="sfoodQ5"]/text()')[0]
        gift_limit = tree.xpath('//*[@id="sgiftQ5"]/text()')[0]
        food = int(float(tree.xpath('//*[@id="foodLimit2"]')[0].text))
        gift = int(float(tree.xpath('//*[@id="giftLimit2"]')[0].text))
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
            await get_content(f"{URL}{use}.html", data={'quality': 5})
        for _ in range(5):
            try:
                data = {"weaponQuality": weaponQuality, "battleRoundId": hidden_id, "side": side, "value": "Berserk"}
                tree, status = await get_content(f"{URL}fight.html", data=data)
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
                await asyncio.sleep(2)
        if not update:  # Error
            break
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
                await get_content(f"{URL}medkit.html", data={})
            else:
                break
        await asyncio.sleep(1)

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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        fight(link, side, weapon_quality, dmg_or_hits, ticketQuality))
    input("Press any key to continue")

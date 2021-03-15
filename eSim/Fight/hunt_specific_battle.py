import asyncio
from random import randint

import __init__  # For IDLE
from Help_functions.bot_functions import send_fight_request
from login import get_content


async def hunt_specific_battle(link, side, max_dmg_for_bh="1", weapon_quality="0"):
    """
    Hunting BH at specific battle.
    (Good for practice / leagues / CW)
    [Might be bugged]"""
    server = link.replace("http://", "https://").split("https://", 1)[1].split(".e-sim.org", 1)[0]
    URL = f"https://{server}.e-sim.org/"
    if side.lower() not in ("defender", "attacker"):
        print(f'"side" must be "defender" or "attacker" (not {side})')
        return
    max_dmg_for_bh = max_dmg_for_bh.replace("k", "000")
    r = await get_content(link.replace("battle", "apiBattles").replace("id", "battleId"))
    while 8 not in (r['defenderScore'], r['attackerScore']):
        r = await get_content(link.replace("battle", "apiBattles").replace("id", "battleId"))
        time_till_round_end = r["hoursRemaining"]*3600 + r["minutesRemaining"]*60 + r["secondsRemaining"] - randint(15, 45)
        print(f"Hunting at {link} ({side}). sleeping for {time_till_round_end} seconds.")
        await asyncio.sleep(time_till_round_end)
        tree = await get_content(link, login_first=True)
        DamageDone = 0
        while DamageDone < int(max_dmg_for_bh):
            Health = int(float(str(tree.xpath("//*[@id='actualHealth']")[0].text)))
            food = tree.xpath('//*[@id="foodLimit2"]')[0].text
            food_limit = tree.xpath('//*[@id="sfoodQ5"]/text()')[0]
            gift = tree.xpath('//*[@id="giftLimit2"]')[0].text
            if Health < 50:
                if int(food) and int(food_limit):
                    await get_content(f"{URL}eat.html", data={'quality': 5})
                else:
                    await get_content(f"{URL}gift.html", data={'quality': 5})
            Damage = 0
            for _ in range(5):
                try:
                    tree, status = await send_fight_request(URL, tree, weapon_quality, side)
                    Damage = int(str(tree.xpath('//*[@id="DamageDone"]')[0].text).replace(",", ""))
                    break
                except:
                    Damage = 0
                    await asyncio.sleep(2)
            DamageDone += Damage
            if DamageDone >= int(max_dmg_for_bh):
                break
            if int(food) == 0 and int(gift) == 0 and Health == 0:
                print("done limits")
                return
            await asyncio.sleep(randint(0, 2))


if __name__ == "__main__":
    print(hunt_specific_battle.__doc__)
    link = input("Battle link: ")
    side = input("Side (attacker/defender: ")
    max_dmg_for_bh = input("Max dmg for bh (write 1 if you are debuff): ")
    weapon_quality = input("Weapon quality (0-5): ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        hunt_specific_battle(link, side, max_dmg_for_bh, weapon_quality))
    input("Press any key to continue")

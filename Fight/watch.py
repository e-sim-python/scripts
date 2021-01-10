import asyncio
import time

import __init__  # For IDLE
from Basic.fly import fly
from login import get_content


async def watch(link, side, start_time="60", keep_wall="3kk", let_overkill="10000000", weaponQuality="5"):
    """
    [might be bugged at the moment]
    Fight at the last minutes of every round in a given battle.

    Examples:
    link="https://alpha.e-sim.org/battle.html?id=1", side="defender" 
    In this example, it will start fighting at t1, it will keep 3kk wall (checking every 10 sec),
    and if enemies did more than 10kk it will pass this round.
    (rest args have default value)
    
    link="https://alpha.e-sim.org/battle.html?id=1", side="defender", start_time=120, keep_wall="5kk", let_overkill="15kk")
    In this example, it will start fighting at t2 (120 sec), it will keep 5kk wall (checking every 10 sec),
    and if enemies did more than 15kk it will pass this round.
    * It will auto fly to bonus region (with Q5 ticket)
    """
    server = link.replace("http://", "https://").split("https://", 1)[1].split(".e-sim.org", 1)[0]
    URL = f"https://{server}.e-sim.org/"
    if side.lower() not in ("defender", "attacker"):
        print(f'"side" must be "defender" or "attacker" (not {side})')
        return
    let_overkill = let_overkill.replace("k", "000")
    keep_wall = keep_wall.replace("k", "000")
    r = await get_content(link.replace("battle", "apiBattles").replace("id", "battleId"))
    if r['type'] == "ATTACK":
        if side.lower() == "attacker":
            try:
                neighboursId = [z['neighbours'] for z in await get_content(
                    f"{URL}apiRegions.html") if z["id"] == r['regionId']][0]
                aBonus = [i for z in await get_content(f'{URL}apiMap.html') for i in neighboursId if
                          i == z['regionId'] and z['occupantId'] == r['attackerId']]
            except:
                aBonus = r['attackerId']
            try:
                await fly(server, aBonus)
            except:
                print("I couldn't find the bonus region")
                return
        elif side.lower() == "defender":
            await fly(server, r['regionId'])
    elif r['type'] == "RESISTANCE":
        await fly(server, r['regionId'])

    while 8 not in (r['defenderScore'], r['attackerScore']):
        r = await get_content(link.replace("battle", "apiBattles").replace("id", "battleId"))
        time_till_round_end = r["hoursRemaining"]*3600 + r["minutesRemaining"]*60 + r["secondsRemaining"] - int(start_time)
        print(f"Sleeping for {time_till_round_end} seconds.")
        await asyncio.sleep(time_till_round_end)
        start = time.time()
        tree = await get_content(link, login_first=True)
        food = tree.xpath('//*[@id="foodLimit2"]')[0].text
        gift = tree.xpath('//*[@id="giftLimit2"]')[0].text
        food_limit = tree.xpath('//*[@id="sfoodQ5"]/text()')[0]
        gift_limit = tree.xpath('//*[@id="sgiftQ5"]/text()')[0]
        print(f"{link}&round={r['currentRound']}\nStarting to hit {food} food ({food_limit}"
              f"in storage) and {gift} gift ({gift_limit} in storage) limits.")

        if time.time() - start > int(start_time):
            break
        if side.lower() == "attacker":
            mySide = int(str(tree.xpath('//*[@id="attackerScore"]/text()')[0]).replace(",", "").strip())
            enemySide = int(str(tree.xpath('//*[@id="defenderScore"]/text()')[0]).replace(",", "").strip())
        else:
            mySide = int(str(tree.xpath('//*[@id="defenderScore"]/text()')[0]).replace(",", "").strip())
            enemySide = int(str(tree.xpath('//*[@id="attackerScore"]/text()')[0]).replace(",", "").strip())
        if enemySide-mySide > int(let_overkill):
            await asyncio.sleep(10)
            continue
        if mySide-enemySide > int(keep_wall):
            await asyncio.sleep(10)
            continue
        hidden_id = tree.xpath("//*[@id='battleRoundId']")[0].value
        Health = int(float(tree.xpath('//*[@id="actualHealth"]')[0].text))
        if Health < 50:
            if int(food) and int(food_limit):
                await get_content(f"{URL}eat.html", data={'quality': 5})
            else:
                await get_content(f"{URL}gift.html", data={'quality': 5})
            if not int(food) and not int(gift):
                print("Done limits")
                return
        else:
            data = {"weaponQuality": weaponQuality, "battleRoundId": hidden_id, "side": side, "value": "Berserk"}
            await get_content(f"{URL}fight.html", data=data)
        if not int(food) and not int(gift) and not Health:
            print("Done limits")
            return
        await asyncio.sleep(0.5)
 
if __name__ == "__main__":
    print(watch.__doc__)
    link = input("Battle link: ")
    side = input("Side (attacker/defender: ")
    start_time = input("When to start hitting (60 means t1): ")
    keep_wall = input("Keep wall (example: 3kk): ")
    let_overkill = input("If enemies leading by this dmg, don't hit: ")
    weapon_quality = input("Weapon quality (0-5): ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        watch(link, side, start_time, keep_wall, let_overkill, weapon_quality))

    input("Press any key to continue")

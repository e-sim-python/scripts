from login import login
import __init__
from Basic.fly import fly

import requests
from lxml.html import fromstring
import time

def watch(link, side, start_time="60", keep_wall="3kk", let_overkill="10000000", weaponQuality="5"):
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
    r = requests.get(link.replace("battle", "apiBattles").replace("id", "battleId")).json()[0]
    while 8 not in (r['defenderScore'], r['attackerScore']):
        r = requests.get(link.replace("battle", "apiBattles").replace("id", "battleId")).json()[0]
        time_till_round_end = r["hoursRemaining"]*3600 + r["minutesRemaining"]*60 + \
                              r["secondsRemaining"] - int(start_time)
        print(f"Sleeping for {time_till_round_end} seconds.")
        time.sleep(time_till_round_end)
        start = time.time()
        session = login(server)
        home_page = session.get(URL)
        tree = fromstring(home_page.content)
        food = tree.xpath('//*[@id="foodLimit2"]')[0].text
        gift = tree.xpath('//*[@id="giftLimit2"]')[0].text
        food_limit = tree.xpath('//*[@id="foodQ5"]/text()')[0]
        gift_limit = tree.xpath('//*[@id="giftQ5"]/text()')[0]
        if r['type'] == "ATTACK":
            if side.lower() == "attacker":
                apiMap = requests.get(f'{URL}apiMap.html').json()
                apiRegions = requests.get(URL + "apiRegions.html").json()
                try:
                    neighboursId = [z['neighbours'] for z in apiRegions if z["id"] == r['regionId']][0]
                    aBonus = [i for z in apiMap for i in neighboursId if i == z['regionId'] and
                              z['occupantId'] == r['attackerId']]
                except:
                    aBonus = r['attackerId']
                try:
                    fly(server, aBonus, session=session)
                except:
                    print("I couldn't find the bonus region")
                    return
            elif side.lower() == "defender":
                fly(server, r['regionId'], session=session)
        elif r['type'] == "RESISTANCE":
            fly(server, r['regionId'], session=session)
        print(f"{link}&round={r['currentRound']}\nStarting to hit {food} food ({food_limit}"
              f"in storage) and {gift} gift ({gift_limit} in storage) limits.")

        if time.time() - start > int(start_time):
            break
        for _ in range(5):
            try:
                r = session.get(link)
                tree = fromstring(r.content)
                if r.status == 200:
                    break
            except:
                time.sleep(0.5)
        if side.lower() == "attacker":
            mySide = int(str(tree.xpath('//*[@id="attackerScore"]/text()')[0]).replace(",", "").strip())
            enemySide = int(str(tree.xpath('//*[@id="defenderScore"]/text()')[0]).replace(",", "").strip())
        else:
            mySide = int(str(tree.xpath('//*[@id="defenderScore"]/text()')[0]).replace(",", "").strip())
            enemySide = int(str(tree.xpath('//*[@id="attackerScore"]/text()')[0]).replace(",", "").strip())
        if enemySide-mySide > int(let_overkill):
            time.sleep(10)
            continue
        if mySide-enemySide > int(keep_wall):
            time.sleep(10)
            continue
        hidden_id = tree.xpath("//*[@id='battleRoundId']")[0].value
        food = tree.xpath('//*[@id="foodLimit2"]')[0].text
        gift = tree.xpath('//*[@id="giftLimit2"]')[0].text
        Health = int(float(tree.xpath('//*[@id="actualHealth"]')[0].text))
        if Health < 50:
            if int(food) and int(food_limit):
                session.post(f"{URL}eat.html?quality=5")
            else:
                session.post(f"{URL}gift.html?quality=5")
            if not int(food) and not int(gift):
                print("Done limits")
                return
        else:
            session.post(f"{URL}fight.html?weaponQuality={weaponQuality}&battleRoundId={hidden_id}&side={side}&value=Berserk")
        if not int(food) and not int(gift) and not Health:
            print("Done limits")
            return
        time.sleep(0.5)
 
if __name__ == "__main__":
    print(watch.__doc__)
    link = input("Battle link: ")
    side = input("Side (attacker/defender: ")
    start_time = input("When to start hitting (60 means t1): ")
    keep_wall = input("Keep wall (example: 3kk): ")
    let_overkill = input("If enemies leading by this dmg, don't hit: ")
    weapon_quality = input("Weapon quality (0-5): ")
    watch(link, side, start_time, keep_wall, let_overkill, weapon_quality)

    input("Press any key to continue")

from login import login

from random import randint
import requests
from lxml.html import fromstring
import time

def hunt_specific_battle(link, side, max_dmg_for_bh="1", weapon_quality="0"):
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
    r = requests.get(link.replace("battle", "apiBattles").replace("id", "battleId")).json()[0]
    while 8 not in (r['defenderScore'], r['attackerScore']):
        r = requests.get(link.replace("battle", "apiBattles").replace("id", "battleId")).json()[0]
        time_till_round_end = r["hoursRemaining"]*3600 + r["minutesRemaining"]*60 +\
                              r["secondsRemaining"] - randint(15, 45)
        print(f"Hunting at {link} ({side}). sleeping for {time_till_round_end} seconds.")
        time.sleep(time_till_round_end)
        session = login(server)
        r = session.get(link)
        tree = fromstring(r.content)
        DamageDone = 0
        while DamageDone < int(max_dmg_for_bh):
            for _ in range(5):
                try:
                    r = session.get(link)
                    tree = fromstring(r.content)
                    if r.status == 200:
                        break
                except:
                    time.sleep(1)
            Health = int(float(str(tree.xpath("//*[@id='actualHealth']")[0].text)))
            hidden_id = tree.xpath("//*[@id='battleRoundId']")[0].value
            food = tree.xpath('//*[@id="foodLimit2"]')[0].text
            food_limit = tree.xpath('//*[@id="sfoodQ5"]/text()')[0]
            gift = tree.xpath('//*[@id="giftLimit2"]')[0].text
            if Health < 50:
                if int(food) and int(food_limit):
                    session.post(f"{URL}eat.html?quality=5")
                else:
                    session.post(f"{URL}gift.html?quality=5")
            Damage = 0
            for _ in range(5):
                try:
                    r = session.post(f"{URL}fight.html?weaponQuality={weapon_quality}&battleRoundId={hidden_id}&side={side}")
                    tree = fromstring(r.content)
                    Damage = int(str(tree.xpath('//*[@id="DamageDone"]')[0].text).replace(",", ""))
                    break
                except:
                    Damage = 0
                    time.sleep(2)
            DamageDone += Damage
            if DamageDone >= int(max_dmg_for_bh):
                break
            if int(food) == 0 and int(gift) == 0 and Health == 0:
                print("done limits")
                return
            time.sleep(randint(0, 2))


if __name__ == "__main__":
    print(hunt_specific_battle.__doc__)
    link = input("Battle link: ")
    side = input("Side (attacker/defender: ")
    max_dmg_for_bh = input("Max dmg for bh (write 1 if you are debuff): ")
    weapon_quality = input("Weapon quality (0-5): ")
    hunt_specific_battle(link, side, max_dmg_for_bh, weapon_quality)
    input("Press any key to continue")

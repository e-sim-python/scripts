from login import login, get_nick_and_pw
import __init__
from Basic.fly import fly

from lxml.html import fromstring
import requests
import time

def hunt(server, maxDmgForBh="500000", startTime="30", weaponQuality="5"):
    """Auto hunt BHs (attack and RWs)"""
    URL = f"https://{server}.e-sim.org/"
    if "t" in startTime.lower():
        startTime = float(startTime.lower().replace("t", "")) * 60
    maxDmgForBh, startTime = int(maxDmgForBh.replace("k", "000")), int(startTime)
    print(f"Startint to hunt at {server}.")
    nick = get_nick_and_pw(server)[0]
    apiCitizen = requests.get(f"{URL}apiCitizenByName.html?name={nick.lower()}").json()
    while 1:
      try:
        battles_time = {}
        apiMap = requests.get(f'{URL}apiMap.html').json()
        for row in apiMap:
            if "battleId" in row:
                apiBattles = requests.get(f'{URL}apiBattles.html?battleId={row["battleId"]}').json()[0]
                round_ends = apiBattles["hoursRemaining"]*3600 + apiBattles["minutesRemaining"]*60 + apiBattles["secondsRemaining"]
                battles_time[row["battleId"]] = round_ends
        apiRegions = requests.get(URL + "apiRegions.html").json()
        for battle_id, round_ends in sorted(battles_time.items(), key=lambda x: x[1]):
            apiBattles = requests.get(f'{URL}apiBattles.html?battleId={battle_id}').json()[0]
            if apiBattles['frozen']:
                continue
            time_to_sleep = apiBattles["hoursRemaining"]*3600 + apiBattles["minutesRemaining"]*60 + apiBattles["secondsRemaining"]
            round_time = 7000 if server in ("primera", "secura", "suna") else 3400
            if time_to_sleep > 7000:
                break
            print("Seconds till next battle:", time_to_sleep)
            try:
                time.sleep(time_to_sleep - startTime)
            except:
                pass
            apiFights = requests.get(f'{URL}apiFights.html?battleId={battle_id}&roundId={apiBattles["currentRound"]}').json()
            defender, attacker = {}, {}
            for hit in apiFights:
                side = defender if hit['defenderSide'] else attacker
                if hit['citizenId'] in side:
                    side[hit['citizenId']] += hit['damage']
                else:
                    side[hit['citizenId']] = hit['damage']

            neighboursId = [region['neighbours'] for region in apiRegions if region["id"] == apiBattles['regionId']]
            if not neighboursId:
                continue  # Not an attack / RW.
            aBonus = [neighbour for region in apiMap for neighbour in neighboursId[0] if neighbour == region['regionId'] and region['occupantId'] == apiBattles['attackerId']]

            def fight(side, DamageDone, session):
                battle = session.get(f'{URL}battle.html?id={battle_id}')
                tree = fromstring(battle.content)
                Health = int(float(str(tree.xpath("//*[@id='actualHealth']")[0].text)))
                hidden_id = tree.xpath("//*[@id='battleRoundId']")[0].value
                food = tree.xpath('//*[@id="foodLimit2"]')[0].text
                gift = tree.xpath('//*[@id="giftLimit2"]')[0].text
                if Health < 50:
                    use = "eat" if int(food) else "gift"
                    session.post(f"{URL}{use}.html", data={'quality': 5})
                battleScore = session.get(f'{URL}battleScore.html?id={hidden_id}&at={apiCitizen["id"]}&ci={apiCitizen["citizenshipId"]}&premium=1').json()
                Damage = 0
                value = "&value=Berserk" if battleScore["spectatorsOnline"] != 1 and Health >= 50 else ""
                for _ in range(5):
                    try:
                        f = session.post(f"{URL}fight.html?weaponQuality={weaponQuality}&battleRoundId={hidden_id}&side={side}{value}")
                        tree = fromstring(f.content)
                        Damage = int(str(tree.xpath('//*[@id="DamageDone"]')[0].text).replace(",", ""))
                        time.sleep(0.3)
                        break
                    except:
                        time.sleep(2)
                try:
                    DamageDone += Damage
                except:
                    print("Couldn't hit")
                if not int(food) and not int(gift) and not Health:
                    print("done limits")
                    DamageDone = 0
                return DamageDone

            def check(side, DamageDone, session):
                battle = session.get(f'{URL}battle.html?id={battle_id}')
                tree = fromstring(battle.content)
                hidden_id = tree.xpath("//*[@id='battleRoundId']")[0].value

                try:
                    sideName = tree.xpath(f"//*[@id='top{side}1']//div//a[1]/text()")[0].strip()
                    sideDMG = int(str(tree.xpath(f'//*[@id="top{side}1"]/div/div[2]')[0].text).replace(",", ""))
                except:
                    sideName, sideDMG = "None", 0
                battleScore = session.get(f'{URL}battleScore.html?id={hidden_id}&at={apiCitizen["id"]}&ci={apiCitizen["citizenshipId"]}&premium=1').json()
                # condition - You are top 1 / did more dmg than your limit / refresh problem                
                condition = (sideName == nick or
                             DamageDone > maxDmgForBh or
                             DamageDone > sideDMG)
                if battleScore["remainingTimeInSeconds"] > startTime:
                    return False
                elif battleScore['spectatorsOnline'] == 1:
                    if sideDMG > maxDmgForBh or condition:
                        return False
                    else:
                        return True
                else:
                    if sideDMG < maxDmgForBh and condition:
                        food = int(tree.xpath('//*[@id="foodLimit2"]')[0].text)
                        use = "eat" if food else "gift"
                        session.post(f"{URL}{use}.html", data={'quality': 5})
                        try:
                            time.sleep(battleScore["remainingTimeInSeconds"] - 13)
                        except:
                            pass
                        battleScore = session.get(f'{URL}battleScore.html?id={hidden_id}&at={apiCitizen["id"]}&ci={apiCitizen["citizenshipId"]}&premium=1').json()
                        if battleScore[f"{side.lower()}sOnline"]:
                            fight(side, DamageDone, session)
                        return False
                    return True

            def hunting(side, side_dmg, session):
                DamageDone = 0
                c = check(side.title(), DamageDone, session)
                while c:
                    DamageDone = fight(side, DamageDone, session)
                    if not DamageDone:  # Done limits or error
                        break
                    if DamageDone > side_dmg:
                        c = check(side.title(), DamageDone, session)
            try:
                aDMG = sorted(attacker.items(), key=lambda x: x[1], reverse=True)[0][1]
            except:
                aDMG = 0
            try:
                dDMG = sorted(defender.items(), key=lambda x: x[1], reverse=True)[0][1]
            except:
                dDMG = 0
            if aDMG < maxDmgForBh or dDMG < maxDmgForBh:
                print(f"Fighting at: {URL}battle.html?id={battle_id}&round={apiBattles['currentRound']}")
                session = login(server)
                if apiBattles['type'] == "ATTACK":
                    if aDMG < maxDmgForBh:
                        try:
                            fly(server, aBonus[0], session=session)
                        except:
                            print("I couldn't find the bonus region")
                            continue
                        side = "attacker"
                        hunting(side, aDMG, session)

                    if dDMG < maxDmgForBh:
                        fly(server, apiBattles['regionId'], session=session)
                        side = "defender"
                        hunting(side, dDMG, session)

                elif apiBattles['type'] == "RESISTANCE":
                    fly(server, apiBattles['regionId'], session=session)
                    if aDMG < maxDmgForBh:
                        side = "attacker"
                        hunting(side, aDMG, session)

                    if dDMG < maxDmgForBh:
                        side = "defender"
                        hunting(side, dDMG, session)
                else:
                    continue
      except Exception as error:
          print(error)
if __name__ == "__main__":
    print(hunt.__doc__)
    server = input("Server: ")
    max_dmg_for_bh = input("Max dmg for bh: ")
    start_time = input("When to start? (If you input 60, it means t1) ")
    weapon_quality = input("Weapon quality (0-5): ")
    hunt(server, max_dmg_for_bh, start_time, weapon_quality)
    input("Press any key to continue")

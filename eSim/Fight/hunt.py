import asyncio

import __init__  # For IDLE
from Basic.fly import fly
from Help_functions.bot_functions import send_fight_request
from login import get_content, get_nick_and_pw


async def hunt(server, maxDmgForBh="500000", startTime="30", weaponQuality="5"):
    """Auto hunt BHs (attack and RWs)"""
    dead_servers = ["primera", "secura", "suna"]
    URL = f"https://{server}.e-sim.org/"
    if "t" in startTime.lower():
        startTime = float(startTime.lower().replace("t", "")) * 60
    maxDmgForBh, startTime = int(maxDmgForBh.replace("k", "000")), int(startTime)
    print(f"Startint to hunt at {server}.")
    nick = get_nick_and_pw(server)[0]
    apiCitizen = await get_content(f"{URL}apiCitizenByName.html?name={nick.lower()}")
    apiRegions = await get_content(URL + "apiRegions.html")
    for _ in range(100):
        try:
            battles_time = {}
            apiMap = await get_content(f'{URL}apiMap.html')
            for row in apiMap:
                if "battleId" in row:
                    apiBattles = await get_content(f'{URL}apiBattles.html?battleId={row["battleId"]}')
                    round_ends = apiBattles["hoursRemaining"] * 3600 + apiBattles["minutesRemaining"] * 60 + apiBattles[
                        "secondsRemaining"]
                    battles_time[row["battleId"]] = round_ends

            for battle_id, round_ends in sorted(battles_time.items(), key=lambda x: x[1]):
                apiBattles = await get_content(f'{URL}apiBattles.html?battleId={battle_id}')
                if apiBattles['frozen']:
                    continue
                time_to_sleep = apiBattles["hoursRemaining"] * 3600 + apiBattles["minutesRemaining"] * 60 + apiBattles[
                    "secondsRemaining"]
                round_time = 7000 if server in ("primera", "secura", "suna") else 3400
                if time_to_sleep > round_time:
                    break
                print("Seconds till next battle:", time_to_sleep)
                try:
                    await asyncio.sleep(time_to_sleep - startTime)
                except:
                    pass
                apiFights = await get_content(f'{URL}apiFights.html?battleId={battle_id}&roundId={apiBattles["currentRound"]}')
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
                aBonus = [neighbour for region in apiMap for neighbour in neighboursId[0] if
                          neighbour == region['regionId'] and region['occupantId'] == apiBattles['attackerId']]

                async def fight(side, DamageDone):
                    tree = await get_content(f'{URL}battle.html?id={battle_id}')
                    Health = int(float(str(tree.xpath("//*[@id='actualHealth']")[0].text)))
                    hidden_id = tree.xpath("//*[@id='battleRoundId']")[0].value
                    food = int(tree.xpath('//*[@id="foodLimit2"]')[0].text)
                    gift = int(tree.xpath('//*[@id="giftLimit2"]')[0].text)
                    if Health < 50:
                        use = "eat" if food else "gift"
                        await get_content(f"{URL}{use}.html", data={'quality': 5})
                    battleScore = await get_content(
                        f'{URL}battleScore.html?id={hidden_id}&at={apiCitizen["id"]}&ci={apiCitizen["citizenshipId"]}&premium=1')
                    Damage = 0
                    if server in dead_servers:
                        value = "Berserk" if battleScore["spectatorsOnline"] != 1 and Health >= 50 else ""
                    else:
                        value = "Berserk"
                    for _ in range(5):
                        try:
                            tree, _ = await send_fight_request(URL, tree, weaponQuality, side, value)
                            Damage = int(str(tree.xpath('//*[@id="DamageDone"]')[0].text).replace(",", ""))
                            await asyncio.sleep(0.3)
                            break
                        except:
                            await asyncio.sleep(2)
                    try:
                        DamageDone += Damage
                    except:
                        print("Couldn't hit")
                    if not food and not gift and not Health:
                        print("done limits")
                        DamageDone = 0
                    return DamageDone

                async def check(side, DamageDone, should_continue):
                    tree = await get_content(f'{URL}battle.html?id={battle_id}')
                    hidden_id = tree.xpath("//*[@id='battleRoundId']")[0].value

                    try:
                        top1Name = tree.xpath(f"//*[@id='top{side}1']//div//a[1]/text()")[0].strip()
                        top1dmg = int(str(tree.xpath(f'//*[@id="top{side}1"]/div/div[2]')[0].text).replace(",", ""))
                    except:
                        top1Name, top1dmg = "None", 0
                    battleScore = await get_content(
                        f'{URL}battleScore.html?id={hidden_id}&at={apiCitizen["id"]}&ci={apiCitizen["citizenshipId"]}&premium=1')
                    # condition - You are top 1 / did more dmg than your limit / refresh problem
                    condition = (top1Name == nick or
                                 DamageDone > maxDmgForBh or
                                 DamageDone > top1dmg)
                    if battleScore["remainingTimeInSeconds"] > startTime:
                        return False
                    elif battleScore['spectatorsOnline'] == 1:
                        if top1dmg > maxDmgForBh or condition:
                            return False
                        else:
                            return True
                    else:
                        if top1dmg < maxDmgForBh and condition:
                            if not should_continue:
                                food = int(tree.xpath('//*[@id="foodLimit2"]')[0].text)
                                use = "eat" if food else "gift"
                                await get_content(f"{URL}{use}.html", data={'quality': 5})
                                try:
                                    await asyncio.sleep(battleScore["remainingTimeInSeconds"] - 13)
                                except:
                                    pass
                                battleScore = await get_content(
                                    f'{URL}battleScore.html?id={hidden_id}&at={apiCitizen["id"]}&ci={apiCitizen["citizenshipId"]}&premium=1')
                                if battleScore[f"{side.lower()}sOnline"]:
                                    await fight(side, DamageDone)
                            return False
                        return True

                async def hunting(side, side_dmg, should_continue):
                    DamageDone = 0
                    c = await check(side.title(), DamageDone, should_continue)
                    while c:
                        DamageDone = await fight(side, DamageDone)
                        if not DamageDone:  # Done limits or error
                            break
                        if DamageDone > side_dmg:
                            c = await check(side.title(), DamageDone, should_continue)

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
                    await get_content(URL, login_first=True)
                    if apiBattles['type'] == "ATTACK":
                        if aDMG < maxDmgForBh:
                            try:
                                await fly(server, aBonus[0])
                            except:
                                print("I couldn't find the bonus region")
                                continue
                            await hunting("attacker", aDMG, dDMG < maxDmgForBh)

                        if dDMG < maxDmgForBh:
                            await fly(server, apiBattles['regionId'])
                            await hunting("defender", dDMG, aDMG < maxDmgForBh)

                    elif apiBattles['type'] == "RESISTANCE":
                        await fly(server, apiBattles['regionId'])
                        if aDMG < maxDmgForBh:
                            await hunting("attacker", aDMG, dDMG < maxDmgForBh)

                        if dDMG < maxDmgForBh:
                            await hunting("defender", dDMG, aDMG < maxDmgForBh)
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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        hunt(server, max_dmg_for_bh, start_time, weapon_quality))
    input("Press any key to continue")

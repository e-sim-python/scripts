import asyncio
from random import randint

import __init__  # For IDLE
from Basic.fly import fly
from Help_functions.bot_functions import fighting, get_battle_id, location, random_sleep
from login import double_click, get_content


async def auto_fight(server, battle_id="", side="attacker", wep="0", food="", gift="", restores="100"):
    """Dumping health at a random time every restore"""
    URL = f"https://{server}.e-sim.org/"
    restores_left = int(restores)
    for _ in range(int(restores)):
        restores_left -= 1
        try:
            if not str(battle_id).replace("0", "").isdigit():
                battle_id = await get_battle_id(server, battle_id)
            print(f'{URL}battle.html?id={battle_id} side: {side}')
            if not battle_id:
                print("Can't fight in any battle. i will check again after the next restore")
                await random_sleep(restores_left)
                continue
            tree = await get_content(URL, login_first=True)
            check = tree.xpath('//*[@id="taskButtonWork"]//@href')  # checking if you can work
            A = randint(1, 4)
            if check and A == 2:  # Don't work as soon as you can (suspicious)
                current_loc = await location(server)
                await double_click(server)
                await fly(server, current_loc)
            apiBattles = await get_content(f"{URL}apiBattles.html?battleId={battle_id}")
            if 8 in (apiBattles['attackerScore'], apiBattles['defenderScore']):
                print("Battle has finished, i will search for another one")
                battle_id = await get_battle_id(server, battle_id)

            tree = await get_content(f'{URL}battle.html?id={battle_id}')
            fight_ability = tree.xpath("//*[@id='newFightView']//div[3]//div[3]//div//text()[1]")
            if any("You can't fight in this battle from your current location." in s for s in fight_ability):
                print("You can't fight in this battle from your current location.")
                return
            await fighting(server, battle_id, side, wep)
            if food:
                await get_content(f"{URL}eat.html", data={'quality': food})
            if gift:
                await get_content(f"{URL}gift.html", data={'quality': gift})
            if food or gift:
                await fighting(server, battle_id, side, wep)
            await random_sleep(restores_left)

        except Exception as error:
            print("error:", error)
            await random_sleep(restores_left)


if __name__ == "__main__":
    print(auto_fight.__doc__)
    server = input("Server: ")
    battle_id = input("Battle id (optional): ")
    if battle_id:
        side = input("Side (attacker/defender): ")
        if side.lower() not in ("attacker", "defender"):
            print(f"'side' parameter must be attacker/defender only (not {side})")
            raise SystemExit()
    else:
        side = "attacker"
    wep = input("Wep quality (0-5): ")
    food = input("If you want to use food, enter it's quality (1-5): ")
    gift = input("If you want to use gift, enter it's quality (1-5): ")
    restores = input("Fight this amount of restores: ") or "100"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        auto_fight(server, battle_id, side, wep, food, gift, restores))
    input("Press any key to continue")

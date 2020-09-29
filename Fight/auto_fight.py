from login import login, double_click
import __init__
from Help_functions._bot_functions import _fighting, _random_sleep, _get_battle_id


from random import randint
import requests
from lxml.html import fromstring

def auto_fight(server, battle_id="", side="attacker", wep="0", food="", gift="", restores="100"):
    """Dumping health at a random time every restore"""
    URL = f"https://{server}.e-sim.org/"
    restores_left = int(restores)
    for _ in range(int(restores)):
        restores_left -= 1
        try:
            session = login(server)
            try:
                int(battle_id)  # user gave valid id
            except:
                battle_id = _get_battle_id(server, battle_id, session)
            print(f'{URL}battle.html?id={battle_id} side: {side}')
            if battle_id:
                home = session.get(URL)
                tree = fromstring(home.content)
                check = tree.xpath('//*[@id="taskButtonWork"]//@href')  # checking if you can work
                A = randint(1, 4)
                if check and A == 2:  # Don't work as soon as you can (suspicious)
                    double_click(server, session)
                apiBattles = requests.get(f"{URL}apiBattles.html?battleId={battle_id}").json()[0]
                if 8 in (apiBattles['attackerScore'], apiBattles['defenderScore']):
                    print("Battle has finished, i will search for another one")
                    battle_id = _get_battle_id(server, battle_id, session)

                battle_request = session.get(f'{URL}battle.html?id={battle_id}')
                tree = fromstring(battle_request.content)
                fight_ability = tree.xpath("//*[@id='newFightView']//div[3]//div[3]//div//text()[1]")
                if any("You can't fight in this battle from your current location." in s for s in fight_ability):
                    print("You can't fight in this battle from your current location.")
                    return
                _fighting(server, battle_id, side, wep, session)
                if food:
                    session.post(f"{URL}eat.html?quality={food}")
                if gift:
                    session.post(f"{URL}gift.html?quality={gift}")
                if food or gift:
                    _fighting(server, battle_id, side, wep, session)
                _random_sleep(restores_left)

            else:
                print("Can't fight in any battle. i will check again after the next restore")
                _random_sleep(restores_left)

        except Exception as error:
            print("error:", error)
            _random_sleep(restores_left)


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
    restores = input("Fight this amount of restores: ")
    if not restores:
        restores = "100"
    auto_fight(server, battle_id, side, wep, food, gift, restores)
    input("Press any key to continue")

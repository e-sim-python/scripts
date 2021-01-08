import asyncio

from login import get_content


async def mpp_dow_attack(server, ID, action, delay_or_battle_link=""):
    """
    Propose MPP / Declaration of war / Attack region.
    Possible after certain delay / after certain battle."""
    URL = f"https://{server}.e-sim.org/"
    if ".e-sim.org/battle.html?id=" in delay_or_battle_link:
        for _ in range(20):
            apiBattles = await get_content(delay_or_battle_link.replace("battle", "apiBattles").replace("id", "battleId"))
            dScore = apiBattles['defenderScore']
            aScore = apiBattles['attackerScore']
            round_ends = apiBattles["hoursRemaining"] * 3600 + apiBattles["minutesRemaining"] * 60 + apiBattles["secondsRemaining"]
            if 8 in (dScore, aScore):
                print("This battle is over")
                return
            elif 7 not in (dScore, aScore):
                await asyncio.sleep(round_ends + 20)
                continue

            else:
                if round_ends > 5:  # long round case, due to e-sim lags.
                    await asyncio.sleep(round_ends)
                    continue
                break

    elif delay_or_battle_link:
        await asyncio.sleep(int(delay_or_battle_link))

    if action == "attack":
        payload = {'action': "ATTACK_REGION", 'regionId': ID, 'attackButton': "Attack"}
    elif action == "mpp":
        payload = {'action': "PROPOSE_ALLIANCE", 'countryId': ID, 'submit': "Propose alliance"}
    elif action == "dow":
        payload = {'action': "DECLARE_WAR", 'countryId': ID, 'submit': "Declare war"}
    else:
        print(f"parameter 'action' MOST be one of those: mpp/dow/attack (not {action})")
        return
    for x in range(5):  # trying 5 times due to e-sim lags.
        url = await get_content(URL + "countryLaws.html", data=payload, login_first=not x)
        print(url)

if __name__ == "__main__":
    print(mpp_dow_attack.__doc__)
    server = input("Server: ")
    action = input("Pls type the action you want (mpp/dow/attack): ").lower()
    ID = input(f"Region id: " if action == "attack" else f"Country id: ")
    delay_or_battle_link = input(
            "If you want specific delay, type that delay in seconds.\n"
            "Type battle link if you want to activate after that battle: ")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        mpp_dow_attack(server, ID, action, delay_or_battle_link))
    input("Press any key to continue")

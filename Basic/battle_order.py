from login import login

def battle_order(server, battle_link, side, session=""):
    """
    Set battle order.
    You can use battle link/id.
    """
    if side.lower() not in ("attacker", "defender"):
        print(f"'side' parameter can be attacker/defender only (not{side})")
        return
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    battle_id = battle_link.split('=')[1].split('&')[0] if 'http' in battle_link else battle_link
    payload = {'action': "SET_ORDERS", 'battleId': f"{battle_id}_{'true' if side.lower() == 'attacker' else 'false'}",
               'submit': "Set orders"}
    send_action = session.post(URL + "militaryUnitsActions.html", data=payload)
    print(send_action.url)
    return session


if __name__ == "__main__":
    print(battle_order.__doc__)
    server = input("Server: ")
    battle_link = input("Battle link: ")
    side = input("Side: ")
    battle_order(server, battle_link, side)
    input("Press any key to continue")

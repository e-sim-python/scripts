from login import login

from random import randint
import time

def wear_unwear(server, ids, action="-", session=""):
    """
    Wear/take off specific EQ IDs.
    Write + as action for wear, - for take off."""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    results = []
    for ID in ids.split(","):
        ID = ID.replace("#", "").strip()
        payload = {'action': "PUT_OFF" if action == "-" else "EQUIP",
                   'itemId': ID.replace("#", "").replace(f"{URL}showEquipment.html?id=", "")}
        send_action = session.post(f"{URL}equipmentAction.html", data=payload)
        time.sleep(randint(1, 2))
        if str(send_action.url) == "http://www.google.com/":
            # e-sim error
            time.sleep(randint(2, 5))
        results.append(f"ID {ID} - {send_action.url}\n")
    print("".join(results))
    return session


if __name__ == "__main__":
    print(wear_unwear.__doc__)
    server = input("Server: ")
    action = input("Wear or take off? (type + or -)")
    ids = input("EQs ids (separated by a comma): ")
    wear_unwear(server, ids, action)
    input("Press any key to continue")

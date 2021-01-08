import asyncio
from random import randint

from login import get_content


async def wear_unwear(server, ids, action="-"):
    """
    Wear/take off specific EQ IDs.
    Write + as action for wear, - for take off."""
    URL = f"https://{server}.e-sim.org/"

    results = []
    ids = [x.strip() for x in ids.split(",") if x.strip()]
    for Index, ID in enumerate(ids):
        ID = ID.replace("#", "").strip()
        payload = {'action': "PUT_OFF" if action == "-" else "EQUIP",
                   'itemId': ID.replace("#", "").replace(f"{URL}showEquipment.html?id=", "")}
        url = await get_content(f"{URL}equipmentAction.html", data=payload, login_first=not Index)
        await asyncio.sleep(randint(1, 2))
        if url == "http://www.google.com/":
            # e-sim error
            await asyncio.sleep(randint(2, 5))
        results.append(f"ID {ID} - {url}\n")
    print("".join(results))

if __name__ == "__main__":
    print(wear_unwear.__doc__)
    server = input("Server: ")
    action = input("Wear or take off? (type + or -)")
    ids = input("EQs ids (separated by a comma): ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        wear_unwear(server, ids, action))
    input("Press any key to continue")

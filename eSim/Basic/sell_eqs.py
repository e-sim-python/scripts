import asyncio

import __init__  # For IDLE
from Basic.wear_unwear import wear_unwear
from login import get_content


async def sell_eqs(server, ids, price, hours):
    """Sell specific EQ ID(s) & reshuffle & upgrade  at auctions."""
    URL = f"https://{server}.e-sim.org/"

    results = []
    ids = [x.strip() for x in ids.split(",") if x.strip()]
    for Index, ID in enumerate(ids):
        ID = ID.replace(URL + "showEquipment.html?id=", "").strip()
        if ID == "reshuffle":
            item = "SPECIAL_ITEM 20"
        elif ID == "upgrade":
            item = "SPECIAL_ITEM 19"
        else:
            item = f"EQUIPMENT {ID}"
        payload = {'action': "CREATE_AUCTION", 'price': price, "id": item, "length": hours, "submit": "Create auction"}
        url = await get_content(URL + "auctionAction.html", data=payload, login_first=not Index)
        if "CREATE_AUCTION_ITEM_EQUIPED" in url:
            await wear_unwear(server, ID, "-")
            url = await get_content(URL + "auctionAction.html", data=payload)
        results.append(f"ID {ID} - {url}\n")
    print("".join(results))

if __name__ == "__main__":
    print(sell_eqs.__doc__)
    server = input("Server: ")
    ids = input("EQs ids (separated by a comma): ")
    price = input("Starting price: ")
    hours = input("Hours: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        sell_eqs(server, ids, price, hours))
    input("Press any key to continue")

import asyncio

from login import get_content


async def donate_eqs(server, ids, receiver_id):
    """
    Donating specific EQ ID(s) to specific user.
    If you need anything else (gold, products) use contract (see accept_contract function)
    """
    URL = f"https://{server}.e-sim.org/"

    results = []
    ids = [x.strip() for x in ids.split(",") if x.strip()]
    for Index, ID in enumerate(ids):
        payload = {"equipmentId": ID.strip(), "id": receiver_id, "reason": " ", "submit": "Donate"}
        url = await get_content(URL + "donateEquipment.html", data=payload, login_first=not Index)
        results.append(f"ID {ID} - {url}")
    print("\n".join(results))

if __name__ == "__main__":
    print(donate_eqs.__doc__)
    server = input("Server: ")
    ids = input("EQs ids (separated by a comma): ")
    receiver_id = int(input("Receiver citizen id: "))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        donate_eqs(server, ids, receiver_id))
    input("Press any key to continue")

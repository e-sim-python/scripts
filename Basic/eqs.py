import asyncio

from login import get_content


async def eqs(server):
    """Shows list of EQs in storage."""
    URL = f"https://{server}.e-sim.org/"
    tree = await get_content(URL + 'storage.html?storageType=EQUIPMENT', login_first=True)
    original_IDs = tree.xpath(f'//*[starts-with(@id, "cell")]/a/text()')
    IDs = [f"[{ID}]({URL}showEquipment.html?id={ID.replace('#', '')})" for ID in original_IDs]
    if sum([len(x) for x in IDs]) > 1000:
        IDs = [ID for ID in original_IDs]
        # Eq id instead of link
    items = tree.xpath(f'//*[starts-with(@id, "cell")]/b/text()')
    results = []
    for ID, Item in zip(IDs, items):
        results.append(f"{ID}: {Item}")
    print("\n".join(results))


if __name__ == "__main__":
    print(eqs.__doc__)
    server = input("Server: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        eqs(server))
    input("Press any key to continue")

from login import login

from lxml.html import fromstring

def eqs(server, session=""):
    """Shows list of EQs in storage."""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)

    EQUIPMENT = session.get(URL + 'storage.html?storageType=EQUIPMENT')
    tree = fromstring(EQUIPMENT.content)
    IDs = tree.xpath(f'//*[starts-with(@id, "cell")]/a/text()')
    IDs = [f"[{ID}]({URL}showEquipment.html?id={ID.replace('#', '')})" for ID in IDs]
    if sum([len(x) for x in IDs]) > 1000:
        IDs = [ID for ID in IDs]
        # Eq id instead of link

    items = tree.xpath(f'//*[starts-with(@id, "cell")]/b/text()')
    results = []
    for ID, Item in zip(IDs, items):
        results.append(f"{ID}: {Item}\n")
    print("".join(results))
    return session


if __name__ == "__main__":
    print(eqs.__doc__)
    server = input("Server: ")
    eqs(server)
    input("Press any key to continue")

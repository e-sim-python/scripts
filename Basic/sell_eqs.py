from login import login
if __name__ == "__main__":
    from wear_unwear import wear_unwear
else:
    from .wear_unwear import wear_unwear

def sell_eqs(server, ids, price, hours, session=""):
    """Sell specific EQ ID(s) & reshuffle & upgrade  at auctions."""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    results = []
    for ID in ids.split(","):
        ID = ID.replace(URL + "showEquipment.html?id=", "").strip()
        if ID == "reshuffle":
            item = "SPECIAL_ITEM 20"
        elif ID == "upgrade":
            item = "SPECIAL_ITEM 19"
        else:
            item = f"EQUIPMENT {ID}"
        payload = {'action': "CREATE_AUCTION", 'price': price, "id": item, "length": hours, "submit": "Create auction"}
        post_auction = session.post(URL + "auctionAction.html", data=payload)
        if "CREATE_AUCTION_ITEM_EQUIPED" in str(post_auction.url):
            wear_unwear(server, ID, "-", session)
            post_auction = session.post(URL + "auctionAction.html", data=payload)
        results.append(f"ID {ID} - {post_auction.url}\n")
    print("".join(results))
    return session


if __name__ == "__main__":
    print(sell_eqs.__doc__)
    server = input("Server: ")
    ids = input("EQs ids (separated by a comma): ")
    price = input("Starting price: ")
    hours = input("Hours: ")
    sell_eqs(server, ids, price, hours)
    input("Press any key to continue")

import asyncio
from datetime import datetime

try:
    import pytz
    game_time = True
except:
    print("We recommend installing pytz (pip install pytz) in order to get e-sim time")
    game_time = False

from login import get_content


async def candidate(server):
    """
    Candidate for congress / president elections.
    It will also auto join to the first party (by members) if necessary."""
    URL = f"https://{server}.e-sim.org/"
    if game_time:
        today = int(datetime.now().astimezone(pytz.timezone('Europe/Berlin')).strftime("%d"))  # game time
    else:
        today = int(datetime.now().strftime("%d"))
    if 1 < today < 5:
        payload = {"action": "CANDIDATE", "presentation": "http://", "submit": "Candidate for president"}
        link = "presidentalElections.html"
    elif 20 < today < 24:
        payload = {"action": "CANDIDATE", "presentation": "http://", "submit": "Candidate for congress"}
        link = "congressElections.html"
    else:
        print("Can't candidate today. Try another time.")
        return

    ID = ""
    try:
        tree = await get_content(URL + "partyStatistics.html?statisticType=MEMBERS", login_first=True)
        ID = str(tree.xpath('//*[@id="esim-layout"]//table//tr[2]//td[3]//@href')[0]).split("=")[1]
        party_payload = {"action": "JOIN", "id": ID, "submit": "Join"}
        url = await get_content(URL + "partyStatistics.html", data=party_payload)
        if str(url) != URL + "?actionStatus=PARTY_JOIN_ALREADY_IN_PARTY":
            print(url)

    except:
        pass

    url = await get_content(URL + link, data=payload, login_first=not ID)
    print(url)

if __name__ == "__main__":
    print(candidate.__doc__)
    server = input("Server: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        candidate(server))
    input("Press any key to continue")

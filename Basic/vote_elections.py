import asyncio
from datetime import datetime

try:
    import pytz
    game_time = True
except:
    print("We recommend installing pytz (pip install pytz) in order to get e-sim time")
    game_time = False

from login import get_content


async def elect(server, your_candidate):
    """Voting in congress / president elections."""
    # Functions in use: login, pytz, datetime (datetime)
    your_candidate = your_candidate.lower()
    URL = f"https://{server}.e-sim.org/"
    if game_time:
        today = int(datetime.now().astimezone(pytz.timezone('Europe/Berlin')).strftime("%d"))  # game time
    else:
        today = int(datetime.now().strftime("%d"))

    if today == 5:
        president = True
        link = "presidentalElections.html"
    elif today == 25:
        president = False
        link = "congressElections.html"
    else:
        print("There are not elections today")
        return

    tree = await get_content(URL + link, login_first=True)
    payload = ""
    for tr in range(2, 43):
        try:
            name = tree.xpath(f'//*[@id="esim-layout"]//tr[{tr}]//td[2]/a/text()')[0].strip().lower()
        except:
            print(f"No such candidate ({your_candidate})")
            return
        if name == your_candidate:
            if president:
                candidateId = tree.xpath(f'//*[@id="esim-layout"]//tr[{tr}]/td[4]/form/input[2]')[0].value
                payload = {'action': "VOTE", 'candidate': candidateId, "submit": "Vote"}
            else:
                candidateId = tree.xpath(f'//*[@id="esim-layout"]//tr[{tr}]//td[5]//*[@id="command"]/input[2]')[0].value
                payload = {'action': "VOTE", 'candidateId': candidateId, "submit": "Vote"}
            break

    if payload:
        url = await get_content(URL + link, data=payload)
        print(url)

if __name__ == "__main__":
    print(elect.__doc__)
    server = input("Server: ")
    candidate = input("I want to vote for this candidate: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        elect(server, candidate))
    input("Press any key to continue")

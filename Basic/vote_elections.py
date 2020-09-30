from login import login

try:
    import pytz
    game_time = True
except:
    print("We recommend installing pytz (pip install pytz) in order to get e-sim time")
    game_time = False
from datetime import datetime
from lxml.html import fromstring

def elect(server, your_candidate, session=""):
    """Voting in congress / president elections."""
    # Functions in use: login, pytz, datetime (datetime)
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
        return session

    if not session:
        session = login(server)

    election_page = session.get(URL + link)
    tree = fromstring(election_page.content)
    payload = ""
    for tr in range(2, 43):
        try:
            name = tree.xpath(f'//*[@id="esim-layout"]//tr[{tr}]//td[2]/a/text()')[0].strip()
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
        post_vote = session.post(URL + link, data=payload)
        print(post_vote.url)
    return session


if __name__ == "__main__":
    print(elect.__doc__)
    server = input("Server: ")
    candidate = input("I want to vote for this candidate: ")
    elect(server, candidate)
    input("Press any key to continue")

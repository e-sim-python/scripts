from login import login

try:
    import pytz
    game_time = True
except:
    print("We recommend installing pytz (pip install pytz) in order to get e-sim time")
    game_time = False
from datetime import datetime
from lxml.html import fromstring

def candidate(server, session=""):
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
        return session

    if not session:
        session = login(server)

    try:
        party = session.get(URL + "partyStatistics.html?statisticType=MEMBERS")
        tree = fromstring(party.content)
        ID = str(tree.xpath('//*[@id="esim-layout"]//table//tr[2]//td[3]//@href')[0]).split("=")[1]
        party_payload = {"action": "JOIN", "id": ID, "submit": "Join"}
        join_party = session.post(URL + "partyStatistics.html", data=party_payload)
        if str(join_party.url) != URL + "?actionStatus=PARTY_JOIN_ALREADY_IN_PARTY":
            print(join_party.url)

    except:
        pass

    send_action = session.post(URL + link, data=payload)
    print(send_action.url)
    return session


if __name__ == "__main__":
    print(candidate.__doc__)
    server = input("Server: ")
    candidate(server)
    input("Press any key to continue")

from login import login

import time
from lxml.html import fromstring
import json

def friends(server, option="online", session=""):
    """Sending friend request to the entire server / all online citizens"""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    if option == "online":
        apiOnline = session.get(f"{URL}apiOnlinePlayers.html").json()
        for row in apiOnline:
            row = json.loads(row)
            try:
                send = session.get(f"{URL}friends.html?action=PROPOSE&id={row['id']}")
                if "PROPOSED_FRIEND_OK" in str(send.url):
                    print("Sent to:", row['login'])
            except Exception as error:
                print("error:", error)
            time.sleep(1)
    else:
        get_pages_count = session.get(URL + 'citizenStatistics.html?statisticType=DAMAGE&countryId=0')
        tree = fromstring(get_pages_count.content)
        last = tree.xpath("//ul[@id='pagination-digg']//li[last()-1]//@href")
        last = last[0].split("page=")[1]
        for page in range(1, int(last) + 1):
            i = session.get(URL + 'citizenStatistics.html?statisticType=DAMAGE&countryId=0&page=' + str(page))
            tree = fromstring(i.content)
            links = tree.xpath("//td/a/@href")
            for link in links:
                try:
                    send = session.get(f"{URL}friends.html?action=PROPOSE&id={link.split('=', 1)[1]}")
                    if "PROPOSED_FRIEND_OK" in str(send.url):
                        print(send.url)
                except Exception as error:
                    print("error:", error)
                time.sleep(1)
    return session


if __name__ == "__main__":
    print(friends.__doc__)
    server = input("Server: ")
    option = input("Send friend request to all active players, or only to those who online right now? (online/all) ")
    friends(server, option)
    input("Press any key to continue")

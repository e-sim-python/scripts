from login import login, get_nick_and_pw
import __init__
from Help_functions._bot_functions import _get_staff_list

import requests  
from lxml.html import fromstring

def _do_not_send_twice(URL, blacklist, contract_name, session):
    contracts = session.get(f'{URL}contracts.html')
    tree = fromstring(contracts.content)
    li = 0
    while 1:
        try:
            li += 1
            line = tree.xpath(f'//*[@id="esim-layout"]//div[2]//ul//li[{li}]/a/text()')
            line1 = tree.xpath(f'//*[@id="esim-layout"]//div[2]//ul//li[{li}]/text()')[1]
            nick = line[1].strip()
            contract_offer_name = line[0].strip()
            if contract_offer_name.lower() == contract_name.lower() and "offered to" in line1:
                blacklist.add(nick)
        except:
            break
    return blacklist

def _remove_rejected(URL, blacklist, session):
    notifications = session.get(URL+'notifications.html?filter=CONTRACTS')
    tree = fromstring(notifications.content)
    try:
        last = tree.xpath("//ul[@id='pagination-digg']//li[last()-1]//@href")[0].split("page=")[1]
    except:
        last = 1
    for page in range(1, int(last)+1):
        notifications = session.get(f'{URL}notifications.html?filter=CONTRACTS&page={page}')
        tree = fromstring(notifications.content)
        for tr in range(2, 22):
            line = tree.xpath(f"//tr[{tr}]//td[2]/text()")
            if "   has rejected your  " in line:
                nick = str(tree.xpath(f"//tr[{tr}]//td[2]//a[1]")[0].text).strip()
                blacklist.add(nick)
    return blacklist

def _get_friends_list(server):
    URL = f"https://{server}.e-sim.org/"
    nick = get_nick_and_pw(server)[0]
    apiCitizen = requests.get(f'{URL}apiCitizenByName.html?name={nick.lower()}').json()

    for page in range(1, 100):
        my_friends = requests.get(f'{URL}profileFriendsList.html?id={apiCitizen["id"]}&page={page}')
        tree = fromstring(my_friends.content)
        for div in range(1, 21):
            friend = tree.xpath(f'//div//div[1]//div[{div}]/a/text()')
            if not friend:
                return
            yield friend[0].strip()
 
def send_contracts(server, contract_id, contract_name):
    """
    Sending specific contract to all your friends.
    Exceptions: If you have already sent them that contract, if they have rejected your previous one,
    or if they are staff members"""
    URL = f"https://{server}.e-sim.org/"
    session = login(server)
    blacklist = _get_staff_list(URL)
    blacklist = _do_not_send_twice(URL, blacklist, contract_name, session)
    blacklist = _remove_rejected(URL, blacklist, session)
    for nick in _get_friends_list(server):
        if nick not in blacklist:
            payload = {'id': contract_id, 'action': "PROPOSE", 'citizenProposedTo': nick, 'submit': 'Propose'}
            for _ in range(10):
                try:
                    b = session.post(URL + "contract.html", data=payload)
                    print(nick, b.url)
                    break  # sent
                except:  # some error
                    pass


if __name__ == "__main__":
    print(send_contracts.__doc__)
    server = input("Server: ")
    contract_id = input("Your contract id: ")
    contract_name = input("Your contract name: ")
    send_contracts(server, contract_id, contract_name)
    input("Press any key to continue")

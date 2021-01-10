import asyncio

import __init__  # For IDLE
from Help_functions.bot_functions import get_staff_list
from login import get_content, get_nick_and_pw


async def _do_not_send_twice(URL, blacklist, contract_name):
    tree = await get_content(f'{URL}contracts.html')
    li = 0
    for _ in range(100):
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


async def _remove_rejected(URL, blacklist):
    tree = await get_content(URL+'notifications.html?filter=CONTRACTS')
    last = tree.xpath("//ul[@id='pagination-digg']//li[last()-1]//@href")
    last = last[0].split('page=', 1)[1]
    for page in range(1, int(last)+1):
        if page != 1:
            tree = await get_content(f'{URL}notifications.html?filter=CONTRACTS&page={page}')
        for tr in range(2, 22):
            if "   has rejected your  " in tree.xpath(f"//tr[{tr}]//td[2]/text()"):
                blacklist.add(str(tree.xpath(f"//tr[{tr}]//td[2]//a[1]")[0].text).strip())
    return blacklist


async def _get_friends_list(server):
    URL = f"https://{server}.e-sim.org/"
    nick = get_nick_and_pw(server)[0]
    apiCitizen = await get_content(f'{URL}apiCitizenByName.html?name={nick.lower()}')

    for page in range(1, 100):
        tree = await get_content(f'{URL}profileFriendsList.html?id={apiCitizen["id"]}&page={page}')
        for div in range(1, 21):
            friend = tree.xpath(f'//div//div[1]//div[{div}]/a/text()')
            if not friend:
                return
            yield friend[0].strip()


async def send_contracts(server, contract_id, contract_name):
    """
    Sending specific contract to all your friends.
    Exceptions: If you have already sent them that contract, if they have rejected your previous one,
    or if they are staff members"""
    URL = f"https://{server}.e-sim.org/"
    blacklist = await get_staff_list(URL)
    blacklist = await _do_not_send_twice(URL, blacklist, contract_name)
    blacklist = await _remove_rejected(URL, blacklist)
    Index = 0
    async for nick in _get_friends_list(server):
        Index += 1
        if nick not in blacklist:
            payload = {'id': contract_id, 'action': "PROPOSE", 'citizenProposedTo': nick, 'submit': 'Propose'}
            for _ in range(10):
                try:
                    b = await get_content(URL + "contract.html", data=payload, login_first=not Index)
                    print(nick, b)
                    break  # sent
                except:  # some error
                    pass


if __name__ == "__main__":
    print(send_contracts.__doc__)
    server = input("Server: ")
    contract_id = input("Your contract id: ")
    contract_name = input("Your contract name: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        send_contracts(server, contract_id, contract_name))
    input("Press any key to continue")

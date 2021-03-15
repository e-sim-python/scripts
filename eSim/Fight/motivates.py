import asyncio

import __init__  # For IDLE
from Fight.supply import supply
from login import get_content


async def send_motivates(server, Type="all"):
    """
    Send motivates.
    * checking first 200 new citizens only.
    * If you not have Q3 food / Q3 gift / Q1 weps when it start - it will try to take some from your MU storage.
    """
    URL = f"https://{server}.e-sim.org/"

    tree = await get_content(URL + 'storage.html?storageType=PRODUCT', login_first=True)
    food = int(tree.xpath('//*[@id="foodQ3"]/text()')[0])
    gift = int(tree.xpath('//*[@id="giftQ3"]/text()')[0])
    weps = 0
    for num in range(2, 52):
        try:
            item = str(tree.xpath(f'//*[@id="resourceInput"]/option[{num}]')[0].text).strip()
            item = item.replace("(available", "").replace(")", "").split(":")
            while "  " in item[0]:
                item[0] = item[0].replace("  ", "")
            if item[0] == "Q1 Weapon":
                weps = int(item[1])
        except:
            break

    storage = []
    if Type in ("all", "wep"):
        if weps > 2:
            storage.append(1)

    if Type in ("all", "food"):
        if food > 1:
            storage.append(2)

    if Type in ("all", "gift"):
        if gift > 0:
            storage.append(3)

    if not storage:
        take_weaps = await supply(server, 15, "Q1 wep")
        if take_weaps:
            storage.append(1)
        take_food = await supply(server, 10, "Q3 food")
        if take_food:
            storage.append(2)
        take_gift = await supply(server, 5, "Q3 gift")
        if take_gift:
            storage.append(3)

    newCitizens_tree = await get_content(URL + 'newCitizens.html?countryId=0')
    start_food = int(newCitizens_tree.xpath('//*[@id="foodLimit2"]')[0].text)
    citizenId = int(newCitizens_tree.xpath("//tr[2]//td[1]/a/@href")[0].split("=")[1])
    checking = list()
    for _ in range(200):  # newest 200 players
        try:
            if len(checking) >= 5:
                break
            tree = await get_content(f'{URL}profile.html?id={citizenId}')
            current_food = int(tree.xpath('//*[@id="foodLimit2"]')[0].text)
            if current_food - start_food == 5:
                print("You have sent too many motivates today!")
                break
            today = int(tree.xpath('//*[@class="sidebar-clock"]/b/text()')[-1].split()[-1])
            birthday = int(tree.xpath(f'//*[@class="profile-row" and span = "Birthday"]/span/text()')[0].split()[-1])
            if today - birthday > 3:
                print("Checked all new players")
                break
            print(f"Checking {URL}profile.html?id={citizenId}")
            if tree.xpath('//*[@id="motivateCitizenButton"]'):
                for num in storage:
                    payload = {'type': num, "submit": "Motivate", "id": citizenId}
                    send = await get_content(f"{URL}motivateCitizen.html?id={citizenId}", data=payload)
                    if "&actionStatus=SUCCESFULLY_MOTIVATED" in send:
                        checking.append(send)
                        print(send)
                        break
            citizenId -= 1
        except Exception as error:
            print("error:", error)

if __name__ == "__main__":
    print(send_motivates.__doc__)
    server = input("Server: ")
    Type = input("Motivate type (food/gift/wep/all): ").lower()
    if not Type:
        Type = "all"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        send_motivates(server, Type))
    input("Press any key to continue")

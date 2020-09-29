from supply import supply
from login import login

from lxml.html import fromstring

def send_motivates(server, Type="all", session=""):
    """
    Send motivates.
    * checking first 200 new citizens only.
    * If you not have Q3 food / Q3 gift / Q1 weps when it start - it will try to take some from your MU storage.
    """
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    storage = session.get(URL + 'storage.html?storageType=PRODUCT')
    tree = fromstring(storage.content)
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
        take_weaps = supply(server, 15, "Q1 wep", session)
        if take_weaps:
            storage.append(1)
        take_food = supply(server, 10, "Q3 food", session)
        if take_food:
            storage.append(2)
        take_gift = supply(server, 5, "Q3 gift", session)
        if take_gift:
            storage.append(3)

    newCitizens = session.get(URL + 'newCitizens.html?countryId=0')
    newCitizens_tree = fromstring(newCitizens.content)
    start_food = int(newCitizens_tree.xpath('//*[@id="foodLimit2"]')[0].text)
    citizenId = int(newCitizens_tree.xpath("//tr[2]//td[1]/a/@href")[0].split("=")[1])
    for _ in range(200):  # newest 200 players
        try:
            profile = session.get(URL + 'profile.html?id=' + str(citizenId))
            tree = fromstring(profile.content)
            current_food = int(tree.xpath('//*[@id="foodLimit2"]')[0].text)
            if current_food - start_food == 5:
                print("You have sent too many motivates today!")
                break
            today = int(tree.xpath('//*[@id="userMenu"]/div/div[1]/div/b[3]/text()')[0].split()[1])
            try:
                birthday = int(
                    tree.xpath("//*[@id='profileTable']//tr//td[1]//div[2]//div[9]//span[1]/text()")[0].split()[1])
            except:
                birthday = int(
                    tree.xpath("//*[@id='profileTable']//tr//td[1]//div[3]//div[9]//span[1]/text()")[0].split()[1])
            if today - birthday > 3:
                print("Checked all new players")
                break
            print("Checking", profile.url)
            if tree.xpath('//*[@id="motivateCitizenButton"]'):
                for num in storage:
                    payload = {'type': num, "submit": "Motivate", "id": citizenId}
                    send = session.post(f"{URL}motivateCitizen.html?id={citizenId}", data=payload)
                    if "&actionStatus=SUCCESFULLY_MOTIVATED" in str(send.url):
                        print(send.url)
                        break
            citizenId -= 1
        except Exception as error:
            print("error:", error)
    return session


if __name__ == "__main__":
    print(send_motivates.__doc__)
    server = input("Server: ")
    Type = input("Motivate type (food/gift/wep/all): ").lower()
    if not Type:
        Type = "all"
    send_motivates(server, Type)
    input("Press any key to continue")

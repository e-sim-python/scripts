import __init__
    
from Basic.fly import fly
from Basic.job import job
from Basic.sell_eqs import sell_eqs
from Basic.send_application import citizenship_or_mu_application

from Fight.auto_fight import auto_fight
from Fight.motivates import send_motivates

from Time_saver.add_friends import friends
from login import login, double_click

import time
import requests
from lxml.html import fromstring
from random import choice, randint


def missions(server, missions_to_complete="ALL", action="ALL", session=""):
    """Finish missions.
    * Leave "action" parameter empty if you don't need it to do specific action.
    * Leave "missions_to_complete" parameter empty if you don't want to complete all missions.
    * "action" must be start / complete / skip / ALL"""
    URL = f"https://{server}.e-sim.org/"
    if action.lower() not in ("start", "complete", "skip", "all"):
        print("action must be `start`/`complete`/`skip`/`ALL`")
        return
    if not session:
        session = login(server)
    if missions_to_complete.lower() != "all":
        if action.lower() != "all":
            if action.lower() == "start":
                c = session.post(URL + "betaMissions.html?action=START", data={"submit": "Mission start"})
                if "MISSION_START_OK" not in str(c.url) and "?action=START" not in str(c.url):
                    print(c.url)
                    return
            if action.lower() == "complete":
                c = session.post(URL + "betaMissions.html?action=COMPLETE", data={"submit": "Receive"})
                if "MISSION_REWARD_OK" not in str(c.url) and "?action=COMPLETE" not in str(c.url):
                    print(c.url)
                    return
            if action.lower() == "skip":
                c = session.post(URL + "betaMissions.html",
                                       data={"action": "SKIP", "submit": "Skip this mission"})
                if "MISSION_SKIPPED" not in str(c.url):
                    print(c.url)
                    return
            print("Done")
            return
    if missions_to_complete.lower() == "all":
        RANGE = 20
    else:
        RANGE = int(missions_to_complete)
    for _ in range(1, RANGE+1):
        try:
            home_page = session.get(URL)
            tree = fromstring(home_page.content)
            check = tree.xpath('//*[@id="taskButtonWork"]//@href')
            if check:
                double_click(server, session=session)
            my_id = str(tree.xpath('//*[@id="userName"]/@href')[0]).split("=")[1]
            try:
                num = int(str(tree.xpath('//*[@id="inProgressPanel"]/div[1]/strong')[0].text).split("#")[1].split(":")[0])
            except:
                # need to collect reward / no more missions
                c = session.post(URL + "betaMissions.html?action=COMPLETE", data={"submit": "Receive"})
                if "MISSION_REWARD_OK" not in str(c.url) and "?action=COMPLETE" not in str(c.url):
                    print(f"No more missions today. Come back tommorrow!")
                    return
                print(c.url)
                continue

            if not num:
                print("You have completed all your missions for today, come back tomorrow!")
                return
            print(f"Mission number {num}")            
            c = session.post(URL + "betaMissions.html?action=START", data={"submit": "Mission start"})
            if "MISSION_START_OK" not in str(c.url):
                c = session.post(URL + "betaMissions.html?action=COMPLETE", data={"submit": "Receive"})
            if "MISSION_REWARD_OK" not in str(c.url) and "?action=COMPLETE" not in str(c.url):
                if num == 1:
                    session.get(URL + "inboxMessages.html")
                    session.get(f"{URL}profile.html?id={my_id}")
                
                elif num in (2, 4, 16, 27, 28, 36, 43, 59):
                    double_click(server, session=session)
                elif num in (3, 7):
                    job(server, session)
                elif num in (5, 26, 32, 35, 38, 40, 47, 51, 53, 64):
                    if num == 31:
                        restores = "3"
                        print(f"Hitting {restores} restores, it might take a while")
                    elif num == 46:
                        restores = "2"
                        print(f"Hitting {restores} restores, it might take a while")
                    auto_fight(server, restores="1")
                elif num == 6:
                    session.post(f"{URL}food.html?quality=1")
                elif num == 8:
                    session.get(URL + "editCitizen.html")
                elif num == 9:
                    session.get(URL + "notifications.html")
                elif num == 10:
                    session.get(URL + "newMap.html")
                elif num == 11:
                    product_market = session.get(f"{URL}productMarket.html")
                    tree = fromstring(product_market.content)
                    productId = tree.xpath('//*[@id="command"]/input[1]')[0].value
                    payload = {'action': "buy", 'id': productId, 'quantity': 1, "submit": "Buy"}
                    session.post(URL + "productMarket.html", data=payload)
                elif num in (12, 54):
                    Citizen = session.get(f'{URL}apiCitizenById.html?id={my_id}').json()
                    apiRegions = session.get(URL + "apiRegions.html").json()
                    capital = [row['id'] if row['homeCountry'] == Citizen['citizenshipId'] and
                                            row['capital'] else 1 for row in apiRegions][0]
                    fly(server, capital, 3, session=session)
                elif num in (13, 66):
                    session.get(URL + 'friends.html?action=PROPOSE&id=8')
                    session.post(URL + "citizenAchievements.html",
                                       data={"id": my_id, "submit": "Recalculate achievements"})
                elif num == 14:
                    i = session.get(URL + 'storage.html?storageType=EQUIPMENT')
                    tree = fromstring(i.content)
                    ID = tree.xpath(f'//*[starts-with(@id, "cell")]/a/text()')[0]
                    payload = {'action': "EQUIP", 'itemId': ID.replace("#", "")}
                    session.post(URL + "equipmentAction.html", data=payload)
                elif num == 15:
                    session.post(f"{URL}vote.html?id=1")
                # day 2
                elif num == 18:
                    shout_body = choice(["Mission: Say hello", "Hi", "Hello", "Hi guys :)", "Mission"])
                    payload = {'action': "POST_SHOUT", 'body': shout_body, 'sendToCountry': "on",
                               "sendToMilitaryUnit": "on", "sendToParty": "on", "sendToFriends": "on"}
                    session.post(f"{URL}shoutActions.html", data=payload)
                elif num == 19:
                    Citizen = session.get(f'{URL}apiCitizenById.html?id={my_id}').json()
                    monetaryMarket = session.get(
                        URL + 'monetaryMarket.html?buyerCurrencyId=0&sellerCurrencyId=' + str(
                            int(Citizen['currentLocationRegionId'] / 6)))
                    tree = fromstring(monetaryMarket.content)
                    ID = tree.xpath("//tr[2]//td[4]//form[1]//input[@value][2]")[0].value
                    payload = {'action': "buy", 'id': ID, 'ammount': 0.5, "submit": "OK"}
                    session.post(URL + "monetaryMarket.html", data=payload)
                elif num == 21:
                    i = session.get(URL + 'storage.html?storageType=EQUIPMENT')
                    tree = fromstring(i.content)
                    ID = tree.xpath(f'//*[starts-with(@id, "cell")]/a/text()')[0].replace("#", "")
                    sell_eqs(server, ID, 0.01, 48, session)
                elif num == 22:
                    Citizen = session.get(f'{URL}apiCitizenById.html?id={my_id}').json()
                    payload = {'product': "GRAIN", 'countryId': Citizen['citizenshipId'], 'storageType': "PRODUCT",
                               "action": "POST_OFFER", "price": 0.1, "quantity": 100}
                    sell_grain = session.post(URL + "storage.html", data=payload)
                    print(sell_grain.url)
                elif num == 25:
                    payload = {'setBg': "LIGHT_I", 'action': "CHANGE_BACKGROUND"}
                    session.post(URL + "editCitizen.html", data=payload)                    
                # day 3
                elif num == 29:
                    for article_id in range(2, 7):
                        session.post(f"{URL}vote.html?id={article_id}")
                elif num == 30:
                    session.post(f"{URL}sub.html?id=1")
                elif num == 31:
                    citizenship_or_mu_application(server, randint(1, 21), "mu", session)
                # day 4
                elif num == 37:
                    shout_body = choice(["Mission: Get to know the community better", "Hi",
                                          "Hello", "Hi guys :)", "Mission", "IRC / Skype / TeamSpeak"])
                    payload = {'action': "POST_SHOUT", 'body': shout_body, 'sendToCountry': "on",
                               "sendToMilitaryUnit": "on", "sendToParty": "on", "sendToFriends": "on"}
                    session.post(f"{URL}shoutActions.html", data=payload)
                elif num == 39:
                    session.get(URL + 'friends.html?action=PROPOSE&id=1')
                elif num == 41:
                    for _ in range(10):
                        ID = randint(1, 100)
                        payload = {"action": "NEW", "key": f"Article {ID}", "submit": "Publish",
                                   "body": choice(["Mission", "Hi", "Hello there", "hello", "Discord?"])}
                        comment = session.post(URL + "comment.html", data=payload)
                        if "MESSAGE_POST_OK" in str(comment.url):
                            break
                elif num == 42:
                    try:
                        b = session.get(URL + "partyStatistics.html?statisticType=MEMBERS")
                        tree = fromstring(b.content)
                        ID = str(tree.xpath('//*[@id="esim-layout"]//table//tr[2]//td[3]//@href')[0]).split("=")[1]
                        payload1 = {"action": "JOIN", "id": ID, "submit": "Join"}
                        b = session.post(URL + "partyStatistics.html", data=payload1)
                        if str(b.url) != URL + "?actionStatus=PARTY_JOIN_ALREADY_IN_PARTY":
                            print(b.url)
                    except:
                        pass
                # day 5
                elif num == 45:
                    session.post(URL + "replyToShout.html?id=1",
                                 data={"body": choice(["OK", "Whatever", "Thanks", "Discord?"]),
                                       "submit": "Shout!"})
                elif num == 46:
                    payload = {'itemType': "STEROIDS", 'storageType': "SPECIAL_ITEM", 'action': "BUY", "quantity": 1}
                    session.post(URL + "storage.html", data=payload)
                elif num == 49:
                    i = session.get(URL + 'storage.html?storageType=EQUIPMENT')
                    tree = fromstring(i.content)
                    ID = tree.xpath(f'//*[starts-with(@id, "cell")]/a/text()')[0]
                    payload = {'action': "EQUIP", 'itemId': ID.replace("#", "")}
                    session.post(URL + "equipmentAction.html", data=payload)
                elif num == 50:
                    session.post(f"{URL}shoutVote.html?id=1&vote=1")
                elif num == 52:
                    fly(server, 1, 3, session)
                elif num == 55:
                    requests.get(URL + f"lan.{my_id}/", verify=False)
                elif num in (61, 55):
                    send_motivates(server, "ALL", session)
                elif num == 57:
                    Citizen = session.get(f'{URL}apiCitizenById.html?id={my_id}').json()
                    payload = {'receiverName': f"{Citizen['citizenship']} Org", "title": "Hi",
                               "body": choice(["Hi", "Can you send me some gold?", "Hello there!", "Discord?"]), "action": "REPLY", "submit": "Send"}
                    session.post(URL + "composeMessage.html", data=payload)

                elif num == 58:
                    session.post(f"{URL}sub.html?id=2")

                elif num == 60:
                    friends(server, "online", session)
                elif num == 63:
                    session.post(f"{URL}medkit.html")
                    # if food & gift limits > 10 it won't work.
                else:
                    print("I don't know how to finish this mission.")
                time.sleep(randint(1, 7))
                c = session.post(URL + "betaMissions.html?action=COMPLETE", data={"submit": "Receive"})
                if "MISSION_REWARD_OK" not in str(c.url) and "?action=COMPLETE" not in str(c.url):
                    c = session.post(URL + "betaMissions.html?action=COMPLETE", data={"submit": "Receive"})
                    if "MISSION_REWARD_OK" not in str(c.url) and "?action=COMPLETE" not in str(c.url):
                        c = session.post(URL + "betaMissions.html",
                                               data={"action": "SKIP", "submit": "Skip this mission"})
                        if "MISSION_SKIPPED" not in str(c.url) and "?action=SKIP" not in str(c.url):
                            return
                        else:
                            print(f"Skipped mission {num}")
            print(c.url)
        except Exception as error:
            print(error)
            time.sleep(5)


if __name__ == "__main__":
    print(missions.__doc__)
    server = input("Server: ")
    missions_to_complete = input("How many missions you wish to complete? (for all of them, press Enter) ")
    if not missions_to_complete:
        missions_to_complete = "all"
    action = input("Action (start / complete / skip / ALL): ")
    if not action:
        action = "all"
    missions(server, missions_to_complete, action)
    input("Press any key to continue")

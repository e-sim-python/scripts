import asyncio
from random import choice, randint

import __init__  # For IDLE
from Basic.fly import fly
from Basic.job import job
from Basic.sell_eqs import sell_eqs
from Basic.send_application import citizenship_or_mu_application
from Fight.auto_fight import auto_fight
from Fight.motivates import send_motivates
from login import double_click, get_content
from Time_saver.add_friends import friends


async def missions(server, missions_to_complete="ALL", action="ALL"):
    """Finish missions.
    * Leave "action" parameter empty if you don't need it to do specific action.
    * Leave "missions_to_complete" parameter empty if you don't want to complete all missions.
    * "action" must be start / complete / skip / ALL"""
    URL = f"https://{server}.e-sim.org/"
    if action.lower() not in ("start", "complete", "skip", "all"):
        print("action must be `start`/`complete`/`skip`/`ALL`")
        return

    if missions_to_complete.lower() != "all":
        if action.lower() != "all":
            if action.lower() == "start":
                c = await get_content(URL + "betaMissions.html?action=START", data={"submit": "Mission start"}, login_first=True)
                if "MISSION_START_OK" not in c and "?action=START" not in c:
                    print(c)
                    return
            if action.lower() == "complete":
                c = await get_content(URL + "betaMissions.html?action=COMPLETE", data={"submit": "Receive"}, login_first=True)
                if "MISSION_REWARD_OK" not in c and "?action=COMPLETE" not in c:
                    print(c)
                    return
            if action.lower() == "skip":
                c = await get_content(URL + "betaMissions.html",
                                      data={"action": "SKIP", "submit": "Skip this mission"}, login_first=True)
                if "MISSION_SKIPPED" not in c:
                    print(c)
                    return
            print("Done")
            return
    if missions_to_complete.lower() == "all":
        RANGE = 20
    else:
        RANGE = int(missions_to_complete)
    for Index in range(RANGE):
        try:
            tree = await get_content(URL, login_first=not Index)
            check = tree.xpath('//*[@id="taskButtonWork"]//@href')
            if check:
                await double_click(server)
            my_id = str(tree.xpath('//*[@id="userName"]/@href')[0]).split("=")[1]
            try:
                num = int(str(tree.xpath('//*[@id="inProgressPanel"]/div[1]/strong')[0].text).split("#")[1].split(":")[0])
            except:
                # need to collect reward / no more missions
                c = await get_content(URL + "betaMissions.html?action=COMPLETE", data={"submit": "Receive"})
                if "MISSION_REWARD_OK" not in c and "?action=COMPLETE" not in c:
                    print(f"No more missions today. Come back tommorrow!")
                    return
                print(c)
                continue

            if not num:
                print("You have completed all your missions for today, come back tomorrow!")
                return
            print(f"Mission number {num}")            
            c = await get_content(URL + "betaMissions.html?action=START", data={"submit": "Mission start"})
            if "MISSION_START_OK" not in c:
                c = await get_content(URL + "betaMissions.html?action=COMPLETE", data={"submit": "Receive"})
            if "MISSION_REWARD_OK" not in c and "?action=COMPLETE" not in c:
                if num == 1:
                    await get_content(URL + "inboxMessages.html")
                    await get_content(f"{URL}profile.html?id={my_id}")
                
                elif num in (2, 4, 16, 27, 28, 36, 43, 59):
                    await double_click(server)
                elif num in (3, 7):
                    await job(server)
                elif num in (5, 26, 32, 35, 38, 40, 47, 51, 53, 64):
                    if num == 31:
                        restores = "3"
                        print(f"Hitting {restores} restores, it might take a while")
                    elif num == 46:
                        restores = "2"
                        print(f"Hitting {restores} restores, it might take a while")
                    await auto_fight(server, restores="1")
                elif num == 6:
                    await get_content(f"{URL}food.html", data={'quality': 1})
                elif num == 8:
                    await get_content(URL + "editCitizen.html")
                elif num == 9:
                    await get_content(URL + "notifications.html")
                elif num == 10:
                    await get_content(URL + "newMap.html")
                elif num == 11:
                    tree = await get_content(f"{URL}productMarket.html")
                    productId = tree.xpath('//*[@id="command"]/input[1]')[0].value
                    payload = {'action': "buy", 'id': productId, 'quantity': 1, "submit": "Buy"}
                    await get_content(URL + "productMarket.html", data=payload)
                elif num in (12, 54):
                    Citizen = await get_content(f'{URL}apiCitizenById.html?id={my_id}')
                    capital = [row['id'] if row['homeCountry'] == Citizen['citizenshipId'] and row[
                        'capital'] else 1 for row in await get_content(URL + "apiRegions.html")][0]
                    await fly(server, capital, 3)
                elif num in (13, 66):
                    await get_content(URL + 'friends.html?action=PROPOSE&id=8')
                    await get_content(URL + "citizenAchievements.html",
                                      data={"id": my_id, "submit": "Recalculate achievements"})
                elif num == 14:
                    tree = await get_content(URL + 'storage.html?storageType=EQUIPMENT')
                    ID = tree.xpath(f'//*[starts-with(@id, "cell")]/a/text()')[0].replace("#", "")
                    payload = {'action': "EQUIP", 'itemId': ID.replace("#", "")}
                    await get_content(URL + "equipmentAction.html", data=payload)
                elif num == 15:
                    await get_content(f"{URL}vote.html", data={"id": 1})
                # day 2
                elif num == 18:
                    shout_body = choice(["Mission: Say hello", "Hi", "Hello", "Hi guys :)", "Mission"])
                    payload = {'action': "POST_SHOUT", 'body': shout_body, 'sendToCountry': "on",
                               "sendToMilitaryUnit": "on", "sendToParty": "on", "sendToFriends": "on"}
                    await get_content(f"{URL}shoutActions.html", data=payload)
                elif num == 19:
                    Citizen = await get_content(f'{URL}apiCitizenById.html?id={my_id}')
                    tree = await get_content(
                        URL + 'monetaryMarket.html?buyerCurrencyId=0&sellerCurrencyId=' + str(
                            int(Citizen['currentLocationRegionId'] / 6)))
                    ID = tree.xpath("//tr[2]//td[4]//form[1]//input[@value][2]")[0].value
                    payload = {'action': "buy", 'id': ID, 'ammount': 0.5, "submit": "OK"}
                    await get_content(URL + "monetaryMarket.html", data=payload)
                elif num == 21:
                    tree = await get_content(URL + 'storage.html?storageType=EQUIPMENT')
                    ID = tree.xpath(f'//*[starts-with(@id, "cell")]/a/text()')[0].replace("#", "")
                    await sell_eqs(server, ID, 0.01, 48)
                elif num == 22:
                    Citizen = await get_content(f'{URL}apiCitizenById.html?id={my_id}')
                    payload = {'product': "GRAIN", 'countryId': Citizen['citizenshipId'], 'storageType': "PRODUCT",
                               "action": "POST_OFFER", "price": 0.1, "quantity": 100}
                    sell_grain = await get_content(URL + "storage.html", data=payload)
                    print(sell_grain)
                elif num == 25:
                    payload = {'setBg': "LIGHT_I", 'action': "CHANGE_BACKGROUND"}
                    await get_content(URL + "editCitizen.html", data=payload)
                # day 3
                elif num == 29:
                    for article_id in range(2, 7):
                        await get_content(f"{URL}vote.html", data={"id": article_id})
                elif num == 30:
                    await get_content(f"{URL}sub.html", data={"id": randint(1, 21)})
                elif num == 31:
                    await citizenship_or_mu_application(server, randint(1, 21), "mu")
                # day 4
                elif num == 37:
                    shout_body = choice(["Mission: Get to know the community better", "Hi",
                                         "Hello", "Hi guys :)", "Mission", "IRC / Skype / TeamSpeak"])
                    payload = {'action': "POST_SHOUT", 'body': shout_body, 'sendToCountry': "on",
                               "sendToMilitaryUnit": "on", "sendToParty": "on", "sendToFriends": "on"}
                    await get_content(f"{URL}shoutActions.html", data=payload)
                elif num == 39:
                    await get_content(URL + 'friends.html?action=PROPOSE&id=1')
                elif num == 41:
                    for _ in range(10):
                        ID = randint(1, 100)
                        payload = {"action": "NEW", "key": f"Article {ID}", "submit": "Publish",
                                   "body": choice(["Mission", "Hi", "Hello there", "hello", "Discord?"])}
                        comment = await get_content(URL + "comment.html", data=payload)
                        if "MESSAGE_POST_OK" in comment:
                            break
                elif num == 42:
                    try:
                        tree = await get_content(URL + "partyStatistics.html?statisticType=MEMBERS")
                        ID = str(tree.xpath('//*[@id="esim-layout"]//table//tr[2]//td[3]//@href')[0]).split("=")[1]
                        payload1 = {"action": "JOIN", "id": ID, "submit": "Join"}
                        b = await get_content(URL + "partyStatistics.html", data=payload1)
                        if b != URL + "?actionStatus=PARTY_JOIN_ALREADY_IN_PARTY":
                            print(b)
                    except:
                        pass
                # day 5
                elif num == 45:
                    await get_content(URL + f"replyToShout.html?id={randint(1, 21)}",
                                      data={"body": choice(["OK", "Whatever", "Thanks", "Discord?"]), "submit": "Shout!"})
                elif num == 46:
                    payload = {'itemType': "STEROIDS", 'storageType': "SPECIAL_ITEM", 'action': "BUY", "quantity": 1}
                    await get_content(URL + "storage.html", data=payload)
                elif num == 49:
                    tree = await get_content(URL + 'storage.html?storageType=EQUIPMENT')
                    ID = tree.xpath(f'//*[starts-with(@id, "cell")]/a/text()')[0].replace("#", "")
                    payload = {'action': "EQUIP", 'itemId': ID.replace("#", "")}
                    await get_content(URL + "equipmentAction.html", data=payload)
                elif num == 50:
                    await get_content(f"{URL}shoutVote.html", data={"id": randint(1, 20), "vote": 1})
                elif num == 52:
                    await fly(server, 1, 3)
                elif num in (61, 55):
                    await send_motivates(server, "ALL")
                elif num == 57:
                    Citizen = await get_content(f'{URL}apiCitizenById.html?id={my_id}')
                    payload = {'receiverName': f"{Citizen['citizenship']} Org", "title": "Hi",
                               "body": choice(["Hi", "Can you send me some gold?", "Hello there!", "Discord?"]), "action": "REPLY", "submit": "Send"}
                    await get_content(URL + "composeMessage.html", data=payload)

                elif num == 58:
                    await get_content(f"{URL}sub.html", data={"id": randint(1, 20)})

                elif num == 60:
                    await friends(server, "online")
                elif num == 63:
                    await get_content(f"{URL}medkit.html", data={})
                    # if food & gift limits >= 10 it won't work.
                else:
                    print(f"I don't know how to finish this mission ({num}).")
                await asyncio.sleep(randint(1, 7))
                c = await get_content(URL + "betaMissions.html?action=COMPLETE", data={"submit": "Receive"})
                if "MISSION_REWARD_OK" not in c and "?action=COMPLETE" not in c:
                    c = await get_content(URL + "betaMissions.html?action=COMPLETE", data={"submit": "Receive"})
                    if "MISSION_REWARD_OK" not in c and "?action=COMPLETE" not in c:
                        c = await get_content(URL + "betaMissions.html",
                                              data={"action": "SKIP", "submit": "Skip this mission"})
                        if "MISSION_SKIPPED" not in c and "?action=SKIP" not in c:
                            return
                        else:
                            print(f"Skipped mission {num}")
            print(c)
        except Exception as error:
            print(error)
            await asyncio.sleep(5)


if __name__ == "__main__":
    print(missions.__doc__)
    server = input("Server: ")
    missions_to_complete = input("How many missions you wish to complete? (for all of them, press Enter) ")
    if not missions_to_complete:
        missions_to_complete = "all"
    action = input("Action (start / complete / skip / ALL): ")
    if not action:
        action = "all"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        missions(server, missions_to_complete, action))
    input("Press any key to continue")

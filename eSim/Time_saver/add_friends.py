import asyncio
from json import loads

from login import get_content


async def friends(server, option="online"):
    """Sending friend request to the entire server / all online citizens"""
    URL = f"https://{server}.e-sim.org/"

    if option == "online":
        for Index, row in enumerate(await get_content(f"{URL}apiOnlinePlayers.html")):
            row = loads(row)
            try:
                url = await get_content(f"{URL}friends.html?action=PROPOSE&id={row['id']}", login_first=not Index, return_url=True)
                if "PROPOSED_FRIEND_OK" in str(url):
                    print("Sent to:", row['login'])
            except Exception as error:
                print("error:", error)
            await asyncio.sleep(1)
    else:
        tree = await get_content(URL + 'citizenStatistics.html?statisticType=DAMAGE&countryId=0')
        last = tree.xpath("//ul[@id='pagination-digg']//li[last()-1]//@href")
        last = last[0].split("page=")[1]
        for page in range(1, int(last) + 1):
            if page != 1:
                tree = await get_content(URL + 'citizenStatistics.html?statisticType=DAMAGE&countryId=0&page=' + str(page))
            for link in tree.xpath("//td/a/@href"):
                try:
                    send = await get_content(f"{URL}friends.html?action=PROPOSE&id={link.split('=')[1]}", return_url=True)
                    if "PROPOSED_FRIEND_OK" in str(send):
                        print(send)
                except Exception as error:
                    print("error:", error)
                await asyncio.sleep(1)

if __name__ == "__main__":
    print(friends.__doc__)
    server = input("Server: ")
    option = input("Send friend request to all active players, or only to those who online right now? (online/all) ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        friends(server, option))
    input("Press any key to continue")

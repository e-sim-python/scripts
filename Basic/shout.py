import asyncio

from login import get_content


async def shout(server, shout_body):
    """Publishing a shout."""
    URL = f"https://{server}.e-sim.org/"

    payload = {'action': "POST_SHOUT", 'body': shout_body, 'sendToCountry': "on",
               "sendToMilitaryUnit": "on", "sendToParty": "on", "sendToFriends": "on"}
    url = await get_content(f"{URL}shoutActions.html", data=payload, login_first=True)
    print(url)

if __name__ == "__main__":
    print(shout.__doc__)
    server = input("Server: ")
    shout_body = input("Shout body: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        shout(server, shout_body))
    input("Press any key to continue")

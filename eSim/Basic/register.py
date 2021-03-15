import asyncio

from aiohttp import ClientSession


async def register(server, nick, password, lan, countryId):
    """User registration."""
    URL = f"https://{server}.e-sim.org/"

    agent = "Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTM Build/LVY48F) CTV"
    headers = {"User-Agent": agent}
    async with ClientSession(headers=headers) as session:
        async with session.get(URL + "index.html?lan=" + lan.replace(f"{URL}lan.", "")) as _:
            login_params = {"preview": "USA_MODERN", "login": nick, "password": password,
                            "mail": f'{nick.replace(" ", "")}@gmail.com', "countryId": countryId, "checkHuman": "Human"}
            async with session.post(URL + "registration.html", data=login_params) as registration:
                print(registration.url)
                if "editAvatar" not in str(registration.url) and URL + "index.html" not in str(registration.url):
                    return print("Could not register")
                print("It's recommended to use avatar and job functions next")
                print(registration.url)

if __name__ == "__main__":
    print(register.__doc__)
    server = input("Server: ")
    nick = input("Nick: ")
    password = input("Password: ")
    lan = input("Your inviter id: ")
    countryId = input("countryId id: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        register(server, nick, password, lan, countryId))
    input("Press any key to continue")

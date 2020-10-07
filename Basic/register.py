from login import login, define_login_details

from lxml.html import fromstring
from random import randint
import requests

def register(server, nick, password, lan, countryId):
    """User registration."""
    URL = f"https://{server}.e-sim.org/"
    try:
        r = requests.get(
            f"https://developers.whatismybrowser.com/useragents/explore/software_name/android-browser/{randint(1, 10)}")
        tree = fromstring(r.content)
        agent = tree.xpath(f"//tr[{randint(1, 50)}]//td[1]/a/text()")[0]
    except:
        agent = "Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTM Build/LVY48F) CTV"
    headers = {"User-Agent": agent, "Referer": "https://e-sim.org"}
    session = requests.session()
    session.headers.update(headers)
    session.get(URL + "index.html?lan=" + lan.replace(f"{URL}lan.", ""))
    login_params = {"preview": "USA_MODERN", "login": nick, "password": password,
                    "mail": f'{nick.replace(" ", "")}@gmail.com', "countryId": countryId, "checkHuman": "Human"}
    registration = session.post(URL + "registration.html", data=login_params)
    if "editAvatar" not in str(registration.url):
        return "Could not register"
    define_login_details(nick, password, server)
    login(server)  # save cookies
    print("We recommend using avatar and job functions next")
    print(registration.url)
    return session


if __name__ == "__main__":
    print(register.__doc__)
    server = input("Server: ")
    nick = input("Nick: ")
    password = input("Password: ")
    lan = input("Your inviter id: ")
    countryId = input("countryId id: ")
    register(server, nick, password, lan, countryId)
    input("Press any key to continue")

import asyncio
import csv
import json
from os import path

from aiohttp import ClientSession
from lxml.html import fromstring

directory = path.dirname(__file__)
loop = asyncio.get_event_loop()

def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)


def define_login_details(nick="", password="", server=""):
    """Saving nicks, passwords for each server from the user, for later use."""
    file_name = path.join(directory, 'login_details.csv')
    if nick and password and server:
        file_exist = path.isfile(file_name)
        with open(file_name, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            if not file_exist:
                writer.writerow(["Server", "Nick", "Password"])
            writer.writerow([server, nick, password])
    if not path.isfile(file_name) or (server and server != "all"):
        with open(file_name, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["Server", "Nick", "Password"])
            print("I will need your nick & password for each server in order to function.")
            print("I will store this data in a local csv (excel) file, so you won't have to write it each time.")
            print(f"(You will be able to edit this file ({file_name}) manually whenever you want)")
            servers = input("Pls write all the servers you want to add (separated by a comma):\n")
            nick, password = "", ""
            for server in servers.split(","):
                server = server.strip().lower()
                if not server:
                    continue
                if nick and password:
                    print(
                        f"If your nick/password for {server} is the same as of the previous server, you can leave that field blank")
                new_nick = input(f"Your nick at {server} (pay attention to uppercase and lowercase letters): ")
                new_password = input(f"Your password at {server} (pay attention to uppercase and lowercase letters): ")
                if new_nick:
                    nick = new_nick
                if new_password:
                    password = new_password
                writer.writerow([server, nick, password])

    cookies_file_name = path.join(directory, 'cookies.txt')
    if not path.isfile(cookies_file_name):
        write_json({}, cookies_file_name)
    with open(cookies_file_name, 'r') as file:
        data = json.load(file)
        try:
            user_agent = data["user_agent"]
        except:
            print("Go to this site - https://www.whatsmyua.info/ , copy your user-agent and paste here")
            user_agent = input(
                "It will tell e-sim that you browsing through your regular browser, so make sure there are no mistakes\n")
        data.update({"user_agent": user_agent})
        write_json(data, cookies_file_name)


def get_nick_and_pw(server):
    nick, password = "", ""
    file_name = path.join(directory, 'login_details.csv')
    all_nicks = {}
    while 1:
        if path.isfile(file_name):
            with open(file_name, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == server or server == "all":
                        nick, password = row[1], row[2]
                        if server == "all":
                            if row[0].lower() != "server":
                                all_nicks[row[0]] = row[1]
                        else:
                            break
        else:
            define_login_details(server=server)

        if nick and password or all_nicks:
            if server == "all":
                return all_nicks
            else:
                return nick, password
        else:
            define_login_details(server=server)


headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}
cookies = {"user_agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}
async def create_session():
    return ClientSession(headers=headers)
session = loop.run_until_complete(create_session())

async def get_content(link, data=None, login_first=False, return_url=False):
    """
    Return types:
    Method post -> respond url (unless fight in link -> tree and url)
    html -> tree (unless return_url is True -> respond url)
    api -> json
    """
    if "api" not in link:
        return_type = "html"
    else:
        return_type = "json"
        login_first = False

    server = link.split("#")[0].replace("http://", "https://").split("https://")[1].split(".e-sim.org")[0]
    method = "get" if data is None else "post"
    if login_first:
        await login(server)
    async with session.get(link, cookies=cookies.get(server), headers=headers, ssl=server!="vita") if method == "get" else \
               session.post(link, cookies=cookies.get(server), headers=headers, data=data, ssl=server!="vita") as respond:
        if method == "post":
            if "fight" in link:
                return fromstring(await respond.text(encoding='utf-8')), respond.status
            return str(respond.url) if not return_url else fromstring(await respond.text(encoding='utf-8'))
        if return_type == "html":
            return fromstring(await respond.text(encoding='utf-8')) if not return_url else str(respond.url)
        else:
            json_respond = await respond.json(content_type=None)
            if "apiBattles" in link:
                return json_respond[0]
            return json_respond


async def login(server, clear_cookies=False):
    """
    Saving cookies and user agent string in a local file (for later use), and replace the cookies if they are too old.
    """
    define_login_details()
    URL = f"https://{server}.e-sim.org/"
    cookies_file_name = path.join(directory, 'cookies.txt')
    if server not in cookies:
        with open(cookies_file_name, 'r') as file:
            cookies.update(json.load(file))
    if clear_cookies and server in cookies:
        del cookies[server]
    user_agent = cookies.get("user_agent", 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0')

    headers.update({"User-Agent": user_agent, "Referer": f"{URL}index.html"})
    online_check = False
    if server in cookies:
        online_check = await session.get(URL + "storage.html", cookies=cookies[server], headers=headers, ssl=server!="vita")
        online_check = "notLoggedIn" in str(online_check.url) or "error" in str(online_check.url)
    if online_check or server not in cookies:
        nick, password = get_nick_and_pw(server)
        payload = {'login': nick, 'password': password, "submit": "Login"}
        async with session.get(URL, headers=headers, ssl=server!="vita") as _:
            async with session.post(URL + "login.html", headers=headers, data=payload, ssl=server!="vita") as r:
                if "index.html?act=login" not in str(r.url):
                    print(r.url)
                    print("Login problem. check your nick and password and try again")
                    exit()
                else:
                    print("Logged successfully")
        cookies.update({server: {cookie.key: cookie.value for cookie in session.cookie_jar}})
        write_json(cookies, cookies_file_name)


async def double_click(server, queue=""):
    URL = f"https://{server}.e-sim.org/"
    if queue == "+":
        payload1 = {'task': "WORK", "action": "put", "submit": "Add plan"}
        payload2 = {'task': "TRAIN", "action": "put", "submit": "Add plan"}
        await get_content(URL + "taskQueue.html", data=payload1, login_first=True)
        await get_content(URL + "taskQueue.html", data=payload2)

    tree = await get_content(URL + "work.html", login_first=queue != "+")
    if tree.xpath('//*[@id="taskButtonWork"]//@href'):
        try:
            region = tree.xpath('//div[1]//div[2]//div[5]//div[1]//div//div[1]//div//div[4]//a/@href')[0].split("=")[1]
            payload = {'countryId': int(int(region) / 6) + (int(region) % 6 > 0), 'regionId': region,
                       'ticketQuality': 5}
            await get_content(URL + "travel.html", data=payload)
        except:
            return print("I couldn't find in which region your work is. Maybe you don't have a job")

        await get_content(URL + "train/ajax", data={"action": "train"})
        print("Trained successfully at", server)
        Tree = await get_content(URL + "work/ajax", data={"action": "work"}, return_url=True)
        if not Tree.xpath('//*[@id="taskButtonWork"]//@href'):
            print("Worked successfully at", server)
        else:
            print("Couldn't work")
    else:
        print("Already worked")


if __name__ == "__main__":
    print(define_login_details.__doc__)
    define_login_details()
    print(login.__doc__)
    print("write the servers you want to work and train in (separated by a comma)")
    servers = input("If you want all of them, press Enter:\n")
    if servers:
        servers = set(servers.split(","))  # random order
        for server in servers:
            loop.run_until_complete(
                double_click(server.strip()))
    else:
        with open(path.join(directory, 'login_details.csv'), 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != "Server":
                    loop.run_until_complete(double_click(row[0]))

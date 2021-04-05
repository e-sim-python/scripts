import csv
import json
from os import path

import requests
from lxml.html import fromstring

directory = path.dirname(__file__)


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


permanent_servers = 'primera', 'secura', 'suna', 'alpha'


def login(server):
    """
    Saving cookies and user agent string in a local file, and replace the cookies if they are too old.
    Usage:
    from login import login
    session = login(server)
    """
    define_login_details()
    URL = f"https://{server}.e-sim.org/"
    cookies_file_name = path.join(directory, 'cookies.txt')
    with open(cookies_file_name, 'r') as file:
        data = json.load(file)
        user_agent = data["user_agent"]

    headers = {"User-Agent": user_agent, "Referer": f"{URL}index.html"}
    session = requests.session()
    session.headers.update(headers)
    if server.lower() not in permanent_servers:
        session.verify = False
    online_check = False
    if server in data:
        old_cookies = requests.utils.cookiejar_from_dict(data[server])
        session.cookies.update(old_cookies)
        online_check = session.get(URL + "storage.html")
        online_check = "notLoggedIn" in str(online_check.url)
    if online_check or server not in data:
        nick, password = get_nick_and_pw(server)
        payload = {'login': nick, 'password': password, 'remember': True}
        session.get(URL)
        r = session.post(URL + "login.html", data=payload)
        if "notLoggedIn" in str(r.url):
            print(r.url)
            print("Login problem. check your nick and password and try again")
            raise SystemExit(0)
        elif "index.html?act=login" in str(r.url):
            print("Logged successfully")
        data.update({server: requests.utils.dict_from_cookiejar(session.cookies)})
        write_json(data, cookies_file_name)

    return session


def double_click(server, queue="", session=""):
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)

    if queue == "+":
        payload1 = {'task': "WORK", "action": "put", "submit": "Add plan"}
        payload2 = {'task': "TRAIN", "action": "put", "submit": "Add plan"}
        session.post(URL + "taskQueue.html", data=payload1)
        session.post(URL + "taskQueue.html", data=payload2)

    work_page = session.get(URL + "work.html")
    tree = fromstring(work_page.content)
    check = tree.xpath('//*[@id="taskButtonWork"]//@href')
    if check:
        try:
            region = tree.xpath('//div[1]//div[2]//div[5]//div[1]//div//div[1]//div//div[4]//a/@href')[0].split("=")[1]
            payload = {'countryId': int(int(region) / 6) + (int(region) % 6 > 0), 'regionId': region,
                       'ticketQuality': 5}
        except:
            print("I couldn't find in which region your work is. Maybe you don't have a job")
        session.post(URL + "travel.html", data=payload)
        session.post(URL + "train/ajax?action=train")
        print("Trained successfully at", server)
        work_link = session.post(URL + "work/ajax?action=work")
        tree = fromstring(work_link.content)
        check = tree.xpath('//*[@id="taskButtonWork"]//@href')
        if not check:
            print("Worked successfully at", server)
        else:
            print("Couldn't work")
    else:
        print("Already worked")
    return session


if __name__ == "__main__":
    print(define_login_details.__doc__)
    define_login_details()
    print(login.__doc__)
    print("write the servers you want to work and train in (separated by a comma)")
    servers = input("If you want all of them, press Enter:\n")
    if servers:
        servers = set(servers.split(","))  # random order
        for server in servers:
            double_click(server.strip())
    else:
        with open(path.join(directory, 'login_details.csv'), 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != "Server":
                    double_click(row[0])

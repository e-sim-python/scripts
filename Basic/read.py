from login import login

from lxml.html import fromstring


def read(server, session=""):
    """Reading all new msgs and notifications + accept friend requests"""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)

    home_page = session.get(URL)
    tree = fromstring(home_page.content)
    msgs = int(str(tree.xpath("//*[@id='inboxMessagesMission']/b")[0].text))
    alerts = int(str(tree.xpath('//*[@id="numero1"]/a/b')[0].text))
    results = []
    if alerts:
        for page in range(1, int(alerts / 20) + 2):
            notifications = session.get(f"{URL}notifications.html?page={page}")
            print(f"{notifications.url}\n")
            tree = fromstring(notifications.content)
            for tr in range(2, alerts + 2):
                try:
                    alert = tree.xpath(f'//tr[{tr}]//td[2]')[0].text_content().strip()
                    alertDate = tree.xpath(f'//tr[{tr}]//td[3]')[0].text_content().strip()
                    if "has requested to add you as a friend" in alert:
                        session.get(URL + str(tree.xpath(f"//tr[{tr}]//td[2]/a[2]/@href")[0]))
                    alerts -= 1
                    results.append(f"{alertDate} - {alert}\n")
                except:
                    break

    if msgs:
        inboxMessages = session.get(URL + "inboxMessages.html")
        results.append(f"{inboxMessages.url}\n")
        tree = fromstring(inboxMessages.content)
        for tr in range(2, msgs + 2):
            AUTHOR = tree.xpath(f'//*[@id="inboxTable"]//tr[{tr}]//td[1]//div/a[2]/text()')[0].strip()
            CONTENT = tree.xpath(f'//*[@id="inboxTable"]//tr[{tr}]//td[2]/div[1]')[0].text_content().strip()
            Title = tree.xpath(f'//*[@id="inboxTable"]//tr[{tr}]//td[2]/b[1]//div')[0].text_content().strip()
            date = str(tree.xpath(f'//*[@id="inboxTable"]//tr[{tr}]//td[3]')[0].text).strip()
            results.append(f"From: {AUTHOR}: {Title}\n{CONTENT}\n{date}")
    print("".join(results))
    return session


if __name__ == "__main__":
    print(read.__doc__)
    server = input("Server: ")
    read(server)
    input("Press any key to continue")

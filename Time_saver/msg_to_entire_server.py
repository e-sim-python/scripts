from login import login
from _bot_functions import _get_staff_list

from lxml.html import fromstring
import time

def send_to_all(server, body, first_page="1", last_page="100"):
    """
    Sending specific message to the entire server.
    - You may want to do that from a multi while hiding your IP
    - Your multi has to be level 7 or more.
    - You should try sending your message manually first, to some inactive guy, in order to see if e-sim blocked some words in it.
    - If your multi got banned, you can start with another one from where the previous stopped."""
    URL = f"https://{server}.e-sim.org/"
    staff = _get_staff_list(URL)
    session = login(server)
    for page in range(int(first_page), int(last_page)+1):
        try:
            i = session.get(f'{URL}citizenStatistics.html?statisticType=DAMAGE&countryId=0&page={page}')
            tree = fromstring(i.content)
            nicks = tree.xpath("//td/a/text()")
            for receiverName in nicks:
                receiverName = receiverName.strip()
                if receiverName not in staff:
                    payload = {'receiverName': receiverName, "title": "Hi", "body": body, "action": "REPLY", "submit": "Send"}
                    b = session.post(URL+"composeMessage.html", data=payload)
                    if "notLoggedIn" in str(b.url):
                        print(f"Sent till page {page} (banned now)")
                        return
                    elif "composeMessage" in str(b.url):
                        if page == int(first_page):
                            print("Looks like e-sim blocked your message, probably because it contain blocked words.")
                            print("Try to find out what that word(s) is, by manually sending the message.")
                            return
                        else:
                            print(f"Error while sending to {receiverName}")
                    else:
                        print(f"Message sent to {receiverName}")
                        
                    time.sleep(10)                                         
        except Exception as error:
            print("error:", error)


if __name__ == "__main__":
    server = input("Server: ")
    print('Write your message now. Write "q" when you finished')
    lines = []
    while 1:
        line = input()
        if line.lower() != "q":
            lines.append(line)
        else:
            break
    body = '\n'.join(lines)
    send_to_all(server, body)

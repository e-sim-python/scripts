import asyncio

from Help_functions.bot_functions import get_staff_list
from login import get_content


async def send_to_all(server, body, first_page="1", last_page="100"):
    """
    Sending specific message to the entire server.
    - You may want to do that from a multi while hiding your IP
    - Your multi has to be level 7 or more.
    - You should try sending your message manually first, to some inactive guy, in order to see if e-sim blocked some words in it.
    - If your multi got banned, you can start with another one from where the previous stopped."""
    URL = f"https://{server}.e-sim.org/"
    staff = get_staff_list(URL)
    for page in range(int(first_page), int(last_page)+1):
        try:
            tree = await get_content(f'{URL}citizenStatistics.html?statisticType=DAMAGE&countryId=0&page={page}', login_first=page == int(first_page))
            for Index, receiverName in enumerate(tree.xpath("//td/a/text()")):
                receiverName = receiverName.strip()
                if receiverName not in staff:
                    payload = {'receiverName': receiverName, "title": "Hi", "body": body, "action": "REPLY", "submit": "Send"}
                    b = await get_content(URL+"composeMessage.html", data=payload, login_first=Index == 1 and page == 1)
                    if "notLoggedIn" in b:
                        print(f"Sent till page {page} (banned?)")
                        return
                    elif "composeMessage" in b:
                        if page == int(first_page):
                            print("Looks like e-sim blocked your message, probably because it contain blocked words.")
                            print("Try to find out what that word(s) is, by manually sending the message.")
                            return
                        else:
                            print(f"Error while sending to {receiverName}")
                    else:
                        print(f"Message sent to {receiverName}")
                        
                    await asyncio.sleep(10)
        except Exception as error:
            print("error:", error)


if __name__ == "__main__":
    server = input("Server: ")
    print('Write your message now. Write "q" when you finished')
    lines = []
    for _ in range(100):
        line = input()
        if line.lower() != "q":
            lines.append(line)
        else:
            break
    body = '\n'.join(lines)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        send_to_all(server, body))

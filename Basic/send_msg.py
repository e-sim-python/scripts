import asyncio

from login import get_content


async def send_msg(server, receiver_name, title, body):
    """Sending a msg."""
    URL = f"https://{server}.e-sim.org/"
    payload = {'receiverName': receiver_name, "title": title, "body": body, "action": "REPLY", "submit": "Send"}
    url = await get_content(URL + "composeMessage.html", data=payload, login_first=True)
    print(url)

if __name__ == "__main__":
    print(send_msg.__doc__)
    server = input("Server: ")
    receiver_name = input("Receiver name: ")
    title = input("Title: ")
    body = input("Message body: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        send_msg(server, receiver_name, title, body))
    input("Press any key to continue")

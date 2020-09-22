from login import login

def send_msg(server, receiver_name, title, body, session=""):
    """Sending a msg."""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)

    payload = {'receiverName': receiver_name, "title": title, "body": body, "action": "REPLY", "submit": "Send"}
    send_action = session.post(URL + "composeMessage.html", data=payload)
    print(send_action.url)
    return session


if __name__ == "__main__":
    print(send_msg.__doc__)
    server = input("Server: ")
    receiver_name = input("Receiver name: ")
    title = input("Title: ")
    body = input("Message body: ")
    send_msg(server, receiver_name, title, body)
    input("Press any key to continue")

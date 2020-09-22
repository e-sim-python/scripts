from login import login

def shout(server, shout_body, session=""):
    """Publishing a shout."""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    payload = {'action': "POST_SHOUT", 'body': shout_body, 'sendToCountry': "on",
               "sendToMilitaryUnit": "on", "sendToParty": "on", "sendToFriends": "on"}
    publish_shout = session.post(f"{URL}shoutActions.html", data=payload)
    print(publish_shout.url)
    return session


if __name__ == "__main__":
    print(shout.__doc__)
    server = input("Server: ")
    shout_body = input("Shout body: ")
    shout(server, shout_body)
    input("Press any key to continue")

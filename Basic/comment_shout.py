from login import login

def comment_shout(server, shout_id, comment_body, session=""):
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    replyToShout = session.post(f"{URL}replyToShout.html?id={shout_id}",
                                data={"body": comment_body, "submit": "Shout!"})
    print(replyToShout.url)
    return session


if __name__ == "__main__":
    print(comment_shout.__doc__)
    server = input("Server: ")
    shout_id = input("Shout id (you can use F12): ")
    comment_body = input("Comment body: ")
    comment_shout(server, shout_id, comment_body)
    input("Press any key to continue")

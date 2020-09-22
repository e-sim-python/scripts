from login import login

def vote_shout(server, shout_id, session=""):
    """Voting a shout (use F12 in the shouts page in order to find it"""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    voting = session.post(f"{URL}shoutVote.html?id={shout_id}&vote=1")
    print(voting.url)
    return session

    
if __name__ == "__main__":
    print(vote_shout.__doc__)
    server = input("Server: ")
    shout_id = input("Shout id: ")
    vote_shout(server, shout_id)
    input("Press any key to continue")

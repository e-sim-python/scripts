from login import login

def sub(server, newspaper_id, session=""):
    """Subscribe to specific newspaper"""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    post_sub = session.post(f"{URL}sub.html?id={newspaper_id}")
    print(post_sub.url)
    return session
    
    
if __name__ == "__main__":
    print(sub.__doc__)
    server = input("Server: ")
    newspaper_id = input("newspaper id: ")
    sub(server, newspaper_id)
    input("Press any key to continue")

import __init__
from login import login
from Basic.fly import fly

def rw(server, region_id, ticket_quality="5", session=""):
    """
    Open RW.
    Note: region can be link or id.
    * It will auto fly to that region."""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    region_link = region_id if "http" in region_id else f"{URL}region.html?id={region_id}"
    fly(server, region_id, ticket_quality, session=session)
    start_rw = session.post(region_link, data={"submit": "startRWbutton"})
    print(start_rw.url)
    return session


if __name__ == "__main__":
    print(rw.__doc__)
    server = input("Server: ")
    ticket_quality = input("Ticket quality (1-5): ")
    region_id = input("Region id: ")
    rw(server, region_id, ticket_quality)
    input("Press any key to continue")

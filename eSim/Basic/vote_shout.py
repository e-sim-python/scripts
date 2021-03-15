import asyncio

from login import get_content


async def vote_shout(server, shout_id):
    """Voting a shout (use F12 in the shouts page in order to find it"""
    URL = f"https://{server}.e-sim.org/"
    url = await get_content(f"{URL}shoutVote.html", data={"id": shout_id, "vote": 1}, login_first=True)
    print(url)

if __name__ == "__main__":
    print(vote_shout.__doc__)
    server = input("Server: ")
    shout_id = int(input("Shout id: "))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        vote_shout(server, shout_id))
    input("Press any key to continue")

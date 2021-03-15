import asyncio

from login import get_content


async def law(server, link_or_id, your_vote):
    """Voting a law"""
    if your_vote.lower() not in ("yes", "no"):
        print(f"Parameter 'vote' can be 'yes' or 'no' only! (not {your_vote})")
        return
    if ".e-sim.org/law.html?id=" not in link_or_id:
        link_or_id = f"https://{server}.e-sim.org/law.html?id=" + link_or_id

    payload = {'action': f"vote{your_vote.capitalize()}", "submit": f"Vote {your_vote.upper()}"}
    url = await get_content(link_or_id, data=payload, login_first=True)
    print(url)

if __name__ == "__main__":
    print(law.__doc__)
    server = input("Server: ")
    link_or_id = input("Law link / id: ")
    your_vote = input("Your vote (yes/no): ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        law(server, link_or_id, your_vote))
    input("Press any key to continue")

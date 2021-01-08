import asyncio

from login import get_content


async def sub(server, newspaper_id):
    """Subscribe to specific newspaper"""
    URL = f"https://{server}.e-sim.org/"

    url = await get_content(f"{URL}sub.html", data={"id": newspaper_id}, login_first=True)
    print(url)

if __name__ == "__main__":
    print(sub.__doc__)
    server = input("Server: ")
    newspaper_id = int(input("newspaper id: "))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        sub(server, newspaper_id))
    input("Press any key to continue")

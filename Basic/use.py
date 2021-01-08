import asyncio

from login import get_content


async def use(server, food_or_gift, quality="5"):
    """Using food or gift"""
    URL = f"https://{server}.e-sim.org/"
    url = await get_content(f"{URL}{food_or_gift.lower().replace('food', 'eat')}.html", data={'quality': quality}, login_first=True)
    print(url)

if __name__ == "__main__":
    print(use.__doc__)
    server = input("Server: ")
    food_or_gift = input("Food / Gift: ")
    quality = input("Quality: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        use(server, food_or_gift, quality))
    input("Press any key to continue")

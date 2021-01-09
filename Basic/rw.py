import asyncio

import __init__  # For IDLE
from Basic.fly import fly
from login import get_content


async def rw(server, region_id, ticket_quality="5"):
    """
    Open RW.
    Note: region can be link or id.
    * It will auto fly to that region."""
    URL = f"https://{server}.e-sim.org/"

    region_link = region_id if "http" in region_id else f"{URL}region.html?id={region_id}"
    await fly(server, region_id, ticket_quality)
    url = await get_content(region_link, data={"submit": "startRWbutton"})
    print(url)

if __name__ == "__main__":
    print(rw.__doc__)
    server = input("Server: ")
    ticket_quality = input("Ticket quality (1-5): ")
    region_id = input("Region id: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        rw(server, region_id, ticket_quality))
    input("Press any key to continue")

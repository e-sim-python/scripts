import asyncio

from login import get_content
from Help_functions.bot_functions import random_sleep, location


async def fly(server, region_id, ticket_quality="5"):
    """
    traveling to a region
    =======================
    to Use Flight Set for drops, enter 2nd region.

    it will travel between 2 regions every 10 mins.(similar to auto_fight)
    if you decide to use limits, it will consume 1 Q5 food and 1 Q5 gift as well.
    """
    URL = f"https://{server}.e-sim.org/"
    if "http" in str(region_id):
        region_id = region_id.split("=")[1]
    payload = {'countryId': int(int(region_id) / 6) + (int(region_id) % 6 > 0), 'regionId': region_id,
               'ticketQuality': ticket_quality}
    url = await get_content(f"{URL}travel.html", data=payload, login_first=True)
    print(url)


async def flight_set(server, region1, region2, ticket_quality="5", limits=True):
    if ticket_quality != "5":
        ticket_health = {1: 40, 2: 30, 3: 20, 4: 10}
        flights_each_restore = int(200 if limits else 100 / ticket_health[int(ticket_quality)])
        health = 100
        food_or_gift = "eat"
        current_region = await location(server)
        use_counter = 2 if limits else 0
        while True:
            for region_id in (region1, region2):
                if int(region_id) == current_region:
                    continue
                else:
                    current_region = int(region_id)

                if flights_each_restore <= 0 and health < ticket_health[int(ticket_quality)]:
                    await random_sleep()
                    health = 100
                    flights_each_restore = int(200 if limits else 100 / ticket_health[int(ticket_quality)])
                    use_counter = 2 if limits else 0

                await fly(server, region_id, ticket_quality)
                flights_each_restore -= 1
                health -= ticket_health[int(ticket_quality)]

                if health <= 50 and use_counter > 0:
                    await get_content(f"https://{server}.e-sim.org/{food_or_gift}.html", data={'quality': 5})
                    health += 50
                    food_or_gift = "gift" if food_or_gift == "eat" else "eat"
                    use_counter -= 1

    while True:
        for region_id in (region1, region2):
            await fly(server, region_id, ticket_quality)
            # You can add some delay between flights, like "time.sleep(1)"
            # (If you do, add also "import time" at the beginning of the file)


if __name__ == "__main__":
    print(fly.__doc__)
    server = input("Server: ")
    ticket_quality = input("Ticket quality (1-5): ").lower().replace("q", "")
    region_id = input("Region id: ")
    region_id2 = input("2nd region id for flight set, otherwise press enter: ")
    loop = asyncio.get_event_loop()
    if region_id2:
        limits = input("Using limits (y/n)? ")
        limits = True if limits.lower().strip() == "y" else False
        loop.run_until_complete(flight_set(server, region_id, region_id2, ticket_quality, limits))
    else:
        loop.run_until_complete(fly(server, region_id, ticket_quality))
    input("Press any key to continue")

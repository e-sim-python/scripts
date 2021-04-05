from login import login

def fly(server, region_id, ticket_quality="5", session=""):
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    if "http" in str(region_id):
        region_id = region_id.split("=")[1]
    payload = {'countryId': int(int(region_id) / 6) + (int(region_id) % 6 > 0), 'regionId': region_id,
               'ticketQuality': ticket_quality}
    travel = session.post(f"{URL}travel.html", data=payload)
    print(travel.url)
    return session

def flight_set(server, region1, region2, ticket_quality="5", session=""):
    if ticket_quality != "5":
        from Help_functions._bot_functions import _random_sleep
        ticket_health = {1: 40, 2: 30, 3: 20, 4: 10}
        flights_each_restore = int(200 / ticket_health[int(ticket_quality)])
        health = 100
        food_or_gift = "food"
        while 1:
            for region_id in (region1, region2):
                session = fly(server, region_id, ticket_quality, session=session)
                flights_each_restore -= 1
                health -= ticket_health[int(ticket_quality)]
                if not flights_each_restore:
                    _random_sleep()
                    health = 100
                    flights_each_restore = int(200 / ticket_health[int(ticket_quality)])
                
                if health <= 50:
                    session = session.post(f"https://{server}.e-sim.org/{food_or_gift}.html?quality=5")
                    health += 50
                    food_or_gift = "gift" if food_or_gift == "food" else "food"
    while 1:
        for region_id in (region1, region2):
            session = fly(server, region_id, ticket_quality, session=session)
            # You can add some delay between flights, like "time.sleep(1)"
            # (If you do, add also "import time" at the beginning of the file)


if __name__ == "__main__":
    print(fly.__doc__)
    server = input("Server: ")
    ticket_quality = input("Ticket quality (1-5): ").lower().replace("q", "")
    region_id = input("Region id: ")
    region_id2 = input("Write another region id if you have a flight set (for non-stop flights), otherwise click enter: ")
    if region_id2:
        flight_set(server, region_id, region_id2)
    fly(server, region_id, ticket_quality)
    input("Press any key to continue")
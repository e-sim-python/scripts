import asyncio

from login import get_content


async def building(server, regionId, quality, Round):
    """Proposing a building law (for presidents)"""
    URL = f"https://{server}.e-sim.org/"
    quality = str(quality).replace("Q", "")
    if "-" in quality:
        quality, productType = quality.split("-")
    else:
        productType = "DEFENSE_SYSTEM"
    regionId = regionId.replace(URL + "region.html?id=", "")

    payload = {'action': "PLACE_BUILDING", 'regionId': regionId, "productType": productType.strip().upper(),
               "quality": quality.strip(), "round": Round, 'submit': "Propose building"}
    url = await get_content(URL + "countryLaws.html", data=payload, login_first=True)
    print(url)

if __name__ == "__main__":
    print(building.__doc__)
    server = input("Server: ")
    ID = input("region id: ")
    quality = input("Building quality (if you want to build an hospital instead, write like that: 5-hospital): ")
    Round = input("At what round would you like to place that building? ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        building(server, ID, quality, Round))
    input("Press any key to continue")

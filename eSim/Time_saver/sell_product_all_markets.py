import asyncio
from random import randint

import __init__  # For IDLE
from Help_functions.bot_functions import fix_product_name
from login import get_content


async def sell_product_all_markets(server, product, price, quantity):
    URL = f"https://{server}.e-sim.org/"
    for _ in range(100):
        how = input("Post via: (sc / profile): ").strip().lower()
        if how not in ("sc", "profile"):
            print(f'You must choose "sc" or "profile" (not {how})')
        elif how == "sc":
            SC_ID = input("Stock Company ID: ")
            break
        else:
            break

    Q, item = fix_product_name(product)
    if not item:
        return print("Invalid product")
    apiCountries = await get_content(URL + "apiCountries.html")
    countries_with_regions = set(x['occupantId'] for x in apiCountries)
    # Sell to countries by A-B, as you would in game.
    Index = -1
    for country in dict(sorted({k["name"]: k["id"] for k in apiCountries}.items())).values():
        if country in countries_with_regions:
            Index += 1
            if how == "profile":
                payload = {'product': f"{Q}-{item}" if Q else item, 'countryId': country, 'storageType': "PRODUCT",
                           "action": "POST_OFFER", "price": price, "quantity": quantity}
                b = get_content(URL + "storage.html", data=payload, login_first=not Index)
            else:
                payload = {'product': f"{Q}-{item}" if Q else item, 'countryId': country, "id": SC_ID, "action": "POST_PRODUCT_OFFER",
                           "price": price, "quantity": quantity, "submit": "Post new offer"}
                b = await get_content(URL + "stockCompanyAction.html", data=payload, login_first=not Index)
            print(b)
            if "POST_PRODUCT_OK" not in b:
                print("There's a problem -", b)
                break
            await asyncio.sleep(randint(0, 3))


if __name__ == "__main__":
    print(sell_product_all_markets.__doc__)
    server = input("Server: ")
    product = input("Product: ")
    price = input("Price: ")
    quantity = input("Quantity: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        sell_product_all_markets(server, product, price, quantity))
    input("Press any key to continue")

import asyncio

import __init__  # For IDLE
from Help_functions.bot_functions import fix_product_name
from login import get_content


async def supply(server, amount, product):
    """Taking specific product from MU storage."""
    URL = f"https://{server}.e-sim.org/"
    Q, item = fix_product_name(product)
    if not item:
        return print("Invalid product!")
    tree = await get_content(URL, login_first=True)
    my_id = str(tree.xpath('//*[@id="userName"]/@href')[0]).split("=")[1]
    payload = {'product': f"{Q}-{item}" if Q else item, 'quantity': amount,
               "reason": " ", "citizen1": my_id, "submit": "Donate"}
    get_supply = await get_content(URL + "militaryUnitStorage.html", data=payload)
    if "DONATE_PRODUCT_FROM_MU_OK" in str(get_supply):
        print("DONATE_PRODUCT_FROM_MU_OK")
        
        print(get_supply)

if __name__ == "__main__":
    print(supply.__doc__)
    server = input("Server: ")
    product = input("Product: ")
    amount = input("Amount: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        supply(server, amount, product))
    input("Press any key to continue")

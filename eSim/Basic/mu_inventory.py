import asyncio

import __init__
from login import get_content

def import_tabulate():
    try:
        from tabulate import tabulate
    except:
        try:
            import subprocess
            subprocess.call(['pip', 'install', "tabulate"])
            from tabulate import tabulate
        except:
            print(f"Couldnt Install the required Package, please type this in your CMD (command prompt):\n\n "
                  f"pip install tabulate")
            input("press enter to exit...")
            return
import_tabulate()


async def MU_Inventory(server, ctx=None):
    """
    shows all of your in-game Military Unit inventory.
    """
    URL = f"https://{server}.e-sim.org/"
    tree = await get_content(f"{URL}militaryUnitStorage.html", login_first=True)
    container_1 = tree.xpath("//div[@class='storage']")
    quantity = [item.xpath("div[1]/text()")[0].strip() for item in container_1]
    products = list()
    for item in container_1:
        name = item.xpath("div[2]/img/@src")[0].replace("//cdn.e-sim.org//img/productIcons/", "").replace(".png", "")
        if name.lower() in ["iron", "grain", "diamonds", "oil", "stone", "wood"]:
            quality = ""
        else:
            quality = item.xpath("div[2]/img/@src")[1].replace(
                "//cdn.e-sim.org//img/productIcons/", "").replace(".png", "")
        products.append(f"{quality.title()} {name}" if quality else f"{name}")
    if ctx is None:
        from tabulate import tabulate
        print(tabulate(zip(products, quantity), headers=["Product", "Quantity"],
                       tablefmt='grid', colalign=("left", "center"), showindex=False))
    else:
        return products, quantity


if __name__ == "__main__":
    print(MU_Inventory.__doc__)
    server = input("Server: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        MU_Inventory(server))
    input("Press any key to continue")

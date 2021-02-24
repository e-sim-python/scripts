import asyncio

import __init__
from login import get_content


async def MU_Inventory(ctx, server):
    """
    shows all of your in-game Military Unit inventory.
    """
    URL = f"https://{server}.e-sim.org/"
    tree = await get_content(f"{URL}militaryUnitStorage.html", login_first=True)
    container_1 = tree.xpath("//div[@class='storage']")
    quantity = list()
    for item in container_1:
        quantity.append(item.xpath("div[1]/text()")[0].strip())
    Products = list()
    for item in container_1:
        name = item.xpath("div[2]/img/@src")[0].replace("//cdn.e-sim.org//img/productIcons/", "").replace(".png", "")
        if name.lower() in ["iron", "grain", "diamonds", "oil", "stone", "wood"]:
            quality = ""
        else:
            quality = item.xpath("div[2]/img/@src")[1].replace("//cdn.e-sim.org//img/productIcons/", "").replace(".png",
                                                                                                                 "")
        if quality:
            Products.append(f"{quality.title()} {name}")
        else:
            Products.append(f"{name}")
    if ctx is None:
        try:
            from tabulate import tabulate
        except:
            def method4(package):
                import subprocess
                subprocess.call(['pip', 'install', package])
                import tabulate

            try:
                method4("tabulate")
            except:
                print(f"Couldnt Install the required Package, please type this in your CMD (command prompt):\n\n "
                      f"pip install tabulate")
                input("press enter to exit...")
                exit()
            input(f"Installed tabulate package, restart the file, press enter to exit...")
            exit()
        Inventory = tabulate(zip(Products, quantity), headers=["Product", "Quantity"], tablefmt='grid',
                             colalign=("left", "center"), showindex=False)
        print(Inventory)
    else:
        return Products, quantity


if __name__ == "__main__":
    print(MU_Inventory.__doc__)
    server = input("Server: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        MU_Inventory(ctx=None, server=server))
    input("Press any key to continue")

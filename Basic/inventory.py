import asyncio

import __init__
from login import get_content


async def Inventory(ctx, server):
    """
    shows all of your in-game inventory.
    """
    URL = f"https://{server}.e-sim.org/"
    tree = await get_content(f"{URL}storage.html?storageType=PRODUCT", login_first=True)
    tree2 = await get_content(f"{URL}storage.html?storageType=SPECIAL_ITEM")
    container_1 = tree.xpath("//div[@class='storage']")
    special_items = tree2.xpath('//div[@class="specialItemInventory"]')
    gold = tree.xpath('//div[@class="sidebar-money"][1]/b/text()')[0]
    quantity = list()
    quantity.append(gold)
    for item in special_items:
        if item.xpath('span/text()'):
            if item.xpath('b/text()')[0].lower() == "medkit":
                quantity.append(item.xpath('span/text()')[0])
            elif "reshuffle" in item.xpath('b/text()')[0].lower():
                quantity.append(item.xpath('span/text()')[0])
            elif "upgrade" in item.xpath('b/text()')[0].lower():
                quantity.append(item.xpath('span/text()')[0])
    for item in container_1:
        quantity.append(item.xpath("div[1]/text()")[0].strip())
    Products = list()
    Products.append(f"Gold")
    for item in special_items:
        if item.xpath('span/text()'):
            if item.xpath('b/text()')[0].lower() == "medkit":
                Products.append(item.xpath('b/text()')[0])
            elif "reshuffle" in item.xpath('b/text()')[0].lower():
                Products.append("Reshuffles")
            elif "upgrade" in item.xpath('b/text()')[0].lower():
                Products.append("Upgrades")
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
    print(Inventory.__doc__)
    server = input("Server: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Inventory(ctx=None, server=server))
    input("Press any key to continue")

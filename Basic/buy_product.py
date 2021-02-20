import asyncio

import __init__  # For IDLE
from Help_functions.bot_functions import fix_product_name
from login import get_content


async def products(server, product, amount):
    """Buy products at the LOCAL market (consider flying first)."""
    URL = f"https://{server}.e-sim.org/"
    quality, product = fix_product_name(product)
    if not quality:
        quality = 5
    if not product:
        return print("Invalid input")
    amount = int(amount)
    MMBought = 0
    tree = await get_content(f"{URL}storage/money", login_first=True)
    keys = [x.strip() for x in tree.xpath("//div//div/text()") if x]
    values = [float(x.strip()) for x in tree.xpath("//div//div/b/text()") if x]
    my_money = dict(zip([x for x in keys if x], values))
    productsBought = 0
    for loop_count in range(5):
        tree = await get_content(f"{URL}productMarket.html?resource={product}&quality={quality}")
        productId = tree.xpath('//*[@id="command"]/input[1]')[0].value
        stock = int(tree.xpath(f"//tr[2]//td[3]/text()")[0])
        raw_cost = tree.xpath(f"//tr[2]//td[4]//text()")
        cost = float(raw_cost[2].strip())
        if not loop_count:
            mm_type = raw_cost[-1].strip()
            if mm_type in my_money:
                MMBought = my_money[mm_type]
        MM_needed = (amount - productsBought) * cost if (amount - productsBought) <= stock else stock * cost
        for _ in range(5):
            if MMBought >= MM_needed:
                break
            tree1 = await get_content(URL + "monetaryMarket.html")
            ID = tree1.xpath("//tr[2]//td[4]//form[1]//input[@value][2]")[0].value
            CC_offer = float(tree1.xpath('//tr[2]//td[2]//b')[0].text)
            cc_quantity = CC_offer if CC_offer < (amount - productsBought) * cost else (amount - productsBought) * cost
            # Todo: No gold case
            payload = {'action': "buy", 'id': ID, 'ammount': cc_quantity}
            url = await get_content(URL + "monetaryMarket.html", data=payload)
            print(url)
            MMBought += cc_quantity

        quantity = int(MMBought / cost) - productsBought
        if quantity > stock:
            quantity = stock
        if quantity > amount:
            quantity = amount
        payload = {'action': "buy", 'id': productId, 'quantity': quantity, "submit": "Buy"}
        url = await get_content(URL + "productMarket.html", data=payload)
        if "POST_PRODUCT_NOT_ENOUGH_MONEY" in str(url):
            break
        print(url)
        productsBought += quantity
        if productsBought >= amount:
            break

if __name__ == "__main__":
    print(products.__doc__)
    server = input("Server: ")
    product = input("Product: ")
    amount = input("Amount: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        products(server, product, amount))
    input("Press any key to continue")

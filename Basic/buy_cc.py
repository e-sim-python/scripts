import asyncio
from random import randint

from login import get_content


async def cc(server, country_id, max_price, buy_amount):
    """
    Buying specific amount of coins, up to a pre-determined price.
    (It can help if there are many small offers, like NPC)"""
    URL = f"https://{server}.e-sim.org/"
    max_price, buy_amount = float(max_price), float(buy_amount)
    bought_amount = 0

    for Index in range(10):  # 10 pages
        tree = await get_content(f"{URL}monetaryMarket.html?buyerCurrencyId={country_id}", login_first=not Index)
        IDs = tree.xpath("//td[4]//form[1]//input[@value][2]")
        IDs = [ID.value for ID in IDs]
        amounts = tree.xpath('//td[2]//b/text()')
        prices = tree.xpath("//td[3]//b/text()")
        for ID, amount, price in zip(IDs, amounts, prices):
            try:
                amount, price = float(amount), float(price)
                if price <= max_price and bought_amount <= buy_amount:
                    payload = {'action': "buy", 'id': ID,
                               'ammount': amount if amount <= buy_amount - bought_amount else buy_amount - bought_amount}
                    url = await get_content(f"{URL}monetaryMarket.html?buyerCurrencyId={country_id}", data=payload)
                    print(url)
                    if "MM_POST_OK_BUY" not in str(url):
                        return
                    else:
                        bought_amount += amount
                    await asyncio.sleep(randint(0, 2))
                    # sleeping for a random time between 0 and 2 seconds. feel free to change it
                else:
                    return
            except Exception as error:
                print(error)
                await asyncio.sleep(5)

if __name__ == "__main__":
    print(cc.__doc__)
    server = input("Server: ")
    country_id = input("Country id: ")
    max_price = float(input("Max price (included): "))
    buy_amount = float(input("How much coins you want to buy? "))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        cc(server, country_id, max_price, buy_amount))
    input("Press any key to continue")

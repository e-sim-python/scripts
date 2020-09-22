from login import login

from lxml.html import fromstring
from random import randint
import time

def cc(server, country_id, max_price, buy_amount, session=""):
    """
    Buying specific amount of coins, up to a pre-determined price.
    (It can help if there are many small offers, like NPC)"""
    URL = f"https://{server}.e-sim.org/"
    max_price, buy_amount = float(max_price), float(buy_amount)
    bought_amount = 0
    if not session:
        session = login(server)
    for _ in range(10):  # 10 pages
        i = session.get(f"{URL}monetaryMarket.html?buyerCurrencyId={country_id}")
        tree = fromstring(i.content)
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
                    post_buy = session.post(f"{URL}monetaryMarket.html?buyerCurrencyId={country_id}", data=payload)
                    print(post_buy.url)
                    if "MM_POST_OK_BUY" not in str(post_buy.url):
                        return session
                    else:
                        bought_amount += amount
                    time.sleep(randint(0, 2))
                    # sleeping for a random time between 0 and 2 seconds. feel free to change it
                else:
                    return session
            except Exception as error:
                print(error)
                time.sleep(5)


if __name__ == "__main__":
    print(cc.__doc__)
    server = input("Server: ")
    country_id = input("Country id: ")
    max_price = float(input("Max price (included): "))
    buy_amount = float(input("How much coins you want to buy? "))
    cc(server, country_id, max_price, buy_amount)
    input("Press any key to continue")

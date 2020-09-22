from login import login
if __name__ == "__main__":
    from _bot_functions import _prices_helper, _converting_raw_price_to_float, _update_auctions_prices_from_csv
else:
    from ._bot_functions import _prices_helper, _converting_raw_price_to_float, _update_auctions_prices_from_csv

from random import randint
import time
from lxml.html import fromstring

def bid_all_auctions(server, session=""):
    """Bidding on all auctions of all EQs in a given server."""
    URL = f"https://{server}.e-sim.org/"
    prices = {'Helmet': {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Q5': 0, 'Q6': 0, 'Q7': 0},
              'Vision': {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Q5': 0, 'Q6': 0, 'Q7': 0},
              'Personal Armor': {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Q5': 0, 'Q6': 0, 'Q7': 0},
              'Pants': {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Q5': 0, 'Q6': 0, 'Q7': 0},
              'Shoes': {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Q5': 0, 'Q6': 0, 'Q7': 0},
              'Lucky charm': {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Q5': 0, 'Q6': 0, 'Q7': 0},
              'Weapon upgrade': {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Q5': 0, 'Q6': 0, 'Q7': 0},
              'Offhand': {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Q5': 0, 'Q6': 0, 'Q7': 0}}

    file_name = f"../Time_saver/auctions_prices_{server}.csv"
    _prices_helper(file_name)
    prices = _update_auctions_prices_from_csv(prices, file_name)
    if not session:
        session = login(server)
    auction_page = URL + "auctions.html?type=EQUIPMENT&page="
    r = session.get(auction_page + "1")
    tree = fromstring(r.content)
    last = tree.xpath("//ul[@id='pagination-digg']//li[last()-1]//@href")
    last = last[0].split('page=', 1)[1]
    for page in range(1, int(last) + 1):
        try:
            r = session.get(auction_page + str(page))
            print(r.url)
            tree = fromstring(r.content)
            links = tree.xpath("//td[5]/a/@href")
            items = tree.xpath('//td[3]/b/text()')
            currentPrices = tree.xpath('//td[4]/b/text()')
            for link, item, currentPrice in zip(links, items, currentPrices):
                item = item.strip()
                Q, item = item.split(" ", 1)
                price = _converting_raw_price_to_float(prices[item][Q])
                if float(currentPrice) > price:
                    continue  # current bid is too high
                payload = {'action': "BID", 'id': link.split('=', 1)[1], 'price': price}
                post_bid = session.post(URL + "auctionAction.html", data=payload)
                print(post_bid.url)
                time.sleep(randint(0, 2))  # sleeping for a random time between 0 and 2 seconds. feel free to change it
        except Exception as error:
            print(error)
            print(f"error at {auction_page + str(page)}")
    return session


if __name__ == "__main__":
    print(bid_all_auctions.__doc__)
    server = input("Server: ")
    bid_all_auctions(server)
    input("Press any key to continue")

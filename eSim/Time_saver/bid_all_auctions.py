import asyncio
from random import randint

import __init__  # For IDLE
from Help_functions.bot_functions import converting_raw_price_to_float, prices_helper, update_auctions_prices_from_csv
from login import get_content


async def bid_all_auctions(server):
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
    await prices_helper(file_name)
    prices = await update_auctions_prices_from_csv(prices, file_name)

    auction_page = URL + "auctions.html?type=EQUIPMENT&page="
    tree = await get_content(auction_page + "1", login_first=True)
    last = tree.xpath("//ul[@id='pagination-digg']//li[last()-1]//@href")
    last = last[0].split('page=', 1)[1]
    for page in range(1, int(last) + 1):
        try:
            print("Checking auctions page", page)
            if page != 1:
                tree = await get_content(auction_page + str(page))
            links = tree.xpath("//td[5]/a/@href")
            items = tree.xpath('//td[3]/b/text()')
            currentPrices = tree.xpath('//td[4]/b/text()')
            for link, item, currentPrice in zip(links, items, currentPrices):
                item = item.strip()
                Q, item = item.split(" ", 1)
                price = await converting_raw_price_to_float(prices[item][Q])
                if float(currentPrice) > price:
                    continue  # current bid is too high
                payload = {'action': "BID", 'id': link.split('=', 1)[1], 'price': price}
                post_bid = await get_content(URL + "auctionAction.html", data=payload)
                print(post_bid)
                await asyncio.sleep(randint(0, 2))  # sleeping for a random time between 0 and 2 seconds. feel free to change it
        except Exception as error:
            print(error)
            print(f"error at {auction_page + str(page)}")

if __name__ == "__main__":
    print(bid_all_auctions.__doc__)
    server = input("Server: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        bid_all_auctions(server))
    input("Press any key to continue")

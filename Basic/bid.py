from login import login

import requests
from lxml.html import fromstring
import time

def bid_specific_auction(server, auction_id_or_link, price, delay=True):
    """Bidding an auction few seconds before it's end"""
    URL = f"https://{server}.e-sim.org/"
    if ".e-sim.org/auction.html?id=" in auction_id_or_link:
        auction_id_or_link = auction_id_or_link.split("=")[1]
    auction_url = requests.get(f"{URL}auction.html?id={auction_id_or_link}")
    tree = fromstring(auction_url.content)
    try:
        auction_time = str(tree.xpath(f'//*[@id="auctionClock{auction_id}"]')[0].text)
    except:
        print("This auction has probably finished. if you think this is mistake -"
              " you are welcome to run the function again, but this time write the delay yourself")
        return
    h, m, s = auction_time.split(":")
    if delay:
        delay_in_seconds = int(h) * 3600 + int(m) * 60 + int(s) - 30
        time.sleep(delay_in_seconds)
    session = login(server)
    payload = {'action': "BID", 'id': auction_id_or_link, 'price': price}
    post_bid = session.post(URL + "auctionAction.html", data=payload)
    print(post_bid.url)
    return session


if __name__ == "__main__":
    print(bid_specific_auction.__doc__)
    server = input("Server: ")
    auction_id = input("Auction id: ")
    price = input("Your bid: ")
    delay = input("Bid near auctions end? (y/n): ")
    bid_specific_auction(server, auction_id, price, delay=False if delay == "n" else True)
    input("Press any key to continue")

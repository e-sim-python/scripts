from login import login
import __init__
from Help_functions._bot_functions import _fix_product_name

import time
from random import randint

def sell_product_all_markets(server, product, price, quantity):
    URL = f"https://{server}.e-sim.org/"
    while 1:
        how = input("Post via: (sc / profile): ").strip().lower()
        if how not in ("sc", "profile"):
            print(f'You must choose "sc" or "profile" (not {how})')
        elif how == "sc":
            SC_ID = input("Stock Company ID: ")
            break
        else:
            break

    Q, item = _fix_product_name(product)
    if Q or item:  # valid product            
        session = login(server)
        
        countries_with_regions = session.get(URL + "apiCountries.html").json()
        countries_with_regions = set(x['occupantId'] for x in countries_with_regions)
        countries = session.get(URL + "apiCountries.html").json()
        # Sell to countries by A-B, as you would in game.
        countries = dict(sorted({k["name"]: k["id"] for k in countries}.items())).values()
        time.sleep(2)
        
        for country in countries:
            if country in countries_with_regions:
                if how == "profile":
                    payload = {'product': f"{Q}-{item}" if Q else item, 'countryId': country, 'storageType': "PRODUCT",
                               "action": "POST_OFFER", "price": price, "quantity": quantity}
                    b = session.post(URL + "storage.html", data=payload)
                else:
                    payload = {'product': f"{Q}-{item}" if Q else item, 'countryId': country, "id": SC_ID, "action": "POST_PRODUCT_OFFER",
                               "price": price, "quantity": quantity, "submit": "Post new offer"}
                    b = session.post(URL + "stockCompanyAction.html", data=payload)       
                print(b.url)
                if "POST_PRODUCT_OK" not in str(b.url):
                    print("There's a problem -", b.url)
                    break
                time.sleep(randint(0, 3))

import __init__
from Help_functions._bot_functions import _fix_product_name
from login import login

from lxml.html import fromstring


def supply(server, amount, product, session=""):
    """Taking specific product from MU storage."""
    URL = f"https://{server}.e-sim.org/"
    Q, item = _fix_product_name(product)
    if Q or item:  # valid product
        if not session:
            session = login(server)
        main_page = session.get(URL)
        tree = fromstring(main_page.content)
        my_id = str(tree.xpath('//*[@id="userName"]/@href')[0]).split("=")[1]
        payload = {'product': f"{Q}-{item}" if Q else item, 'quantity': amount,
                   "reason": " ", "citizen1": my_id, "submit": "Donate"}
        get_supply = session.post(URL + "militaryUnitStorage.html", data=payload)
        if "DONATE_PRODUCT_FROM_MU_OK" in str(get_supply.url):
            print("DONATE_PRODUCT_FROM_MU_OK")
        
        print(get_supply.url)
        return session


if __name__ == "__main__":
    print(supply.__doc__)
    server = input("Server: ")
    product = input("Product: ")
    amount = input("Amount: ")
    supply(server, amount, product)
    input("Press any key to continue")

from login import login
if __name__ == "__main__":
    from _bot_functions import _fix_product_name
else:
    from ._bot_functions import _fix_product_name

from lxml.html import fromstring

def products(server, product, amount, session=""):
    """Buy products at the LOCAL market (consider flying first)."""
    URL = f"https://{server}.e-sim.org/"
    quality, product = _fix_product_name(product)
    if not quality:
        quality = 5
    if quality or product:  # valid
        if not session:
            session = login(server)
        MMBought = 0
        my_money_page = session.get(f"{URL}storage/money")
        tree = fromstring(my_money_page.content)
        keys = [x.strip() for x in tree.xpath("//div//div/text()") if x]
        values = [float(x.strip()) for x in tree.xpath("//div//div/b/text()") if x]
        my_money = dict(zip([x for x in keys if x], values))
        productsBought = 0
        for loop_count in range(5):
            productMarket = session.get(f"{URL}productMarket.html?resource={product}&quality={quality}")
            tree = fromstring(productMarket.content)
            productId = tree.xpath('//*[@id="command"]/input[1]')[0].value
            stock = int(tree.xpath(f"//tr[2]//td[3]/text()")[0])
            raw_cost = tree.xpath(f"//tr[2]//td[4]//text()")
            cost = float(raw_cost[2].strip())            
            if not loop_count:
                mm_type = raw_cost[-1].strip()
                if mm_type in my_money:
                    MMBought = my_money[mm_type]
            MM_needed = (int(amount) - productsBought) * cost if (int(
                amount) - productsBought) <= stock else stock * cost
            for _ in range(5):
                if MMBought >= MM_needed:
                    break
                monetaryMarket = session.get(URL + "monetaryMarket.html")
                tree = fromstring(monetaryMarket.content)
                ID = tree.xpath("//tr[2]//td[4]//form[1]//input[@value][2]")[0].value
                CC_offer = float(tree.xpath('//tr[2]//td[2]//b')[0].text)
                cc_quantity = CC_offer if CC_offer < (int(amount) - productsBought) * cost else (int
                    amount) - productsBought) * cost
                # Todo: No gold case
                payload = {'action': "buy", 'id': ID, 'ammount': cc_quantity}
                buy_cc = session.post(URL + "monetaryMarket.html", data=payload)
                print(buy_cc.url)
                MMBought += cc_quantity

            quantity = int(MMBought / cost) - productsBought
            if quantity > stock:
                quantity = stock
            if quantity > int(amount):
                quantity = int(amount)
            payload = {'action': "buy", 'id': productId, 'quantity': quantity, "submit": "Buy"}
            buy_product = session.post(URL + "productMarket.html", data=payload)
            if "POST_PRODUCT_NOT_ENOUGH_MONEY" in str(buy_product.url):
                break  # won't happen
            print(buy_product.url)
            productsBought += quantity
            if productsBought >= int(amount):
                break
    return session


if __name__ == "__main__":
    print(products.__doc__)
    server = input("Server: ")
    product = input("Product: ")
    amount = input("Amount: ")
    products(server, product, amount)
    input("Press any key to continue")

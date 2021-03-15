import asyncio

from login import get_content, get_nick_and_pw


async def mm(server):
    """Sells all currencies in your account in the appropriate markets & edit current offers if needed."""
    URL = f"https://{server}.e-sim.org/"
    api = await get_content(URL + "apiCountries.html")
    storage_tree = await get_content(URL + "storage.html?storageType=MONEY", login_first=True)
    for i in range(2, 20):
        try:
            CC = storage_tree.xpath(f'//*[@id="storageConteiner"]//div//div//div//div[{i}]/text()')[-1].strip()
            cc = [i["id"] for i in api if i["currencyName"] == CC][0]
            value = storage_tree.xpath(f'//*[@id="storageConteiner"]//div//div//div//div[{i}]/b/text()')[0]
            tree = await get_content(f'{URL}monetaryMarket.html?buyerCurrencyId={cc}&sellerCurrencyId=0')
            try:
                MM = str(tree.xpath("//tr[2]//td[3]/b")[0].text).strip()
            except:
                MM = 0.1
            payload = {"offeredMoneyId": cc, "buyedMoneyId": 0, "value": value,
                       "exchangeRatio": round(float(MM) - 0.0001, 4), "submit": "Post new offer"}
            send_monetary_market = await get_content(URL + "monetaryMarket.html?action=post", data=payload)
            print(send_monetary_market)
        except:
            break
    nick = get_nick_and_pw(server)[0]
    tree = await get_content(URL + "monetaryMarket.html")
    IDs = tree.xpath('//*[@id="command"]//input[1]')
    for i in range(2, 20):
        try:
            CC = tree.xpath(f'//*[@id="esim-layout"]//table[2]//tr[{i}]//td[1]/text()')[-1].strip()
            cc = [i["id"] for i in api if i["currencyName"] == CC][0]
            tree = await get_content(f'{URL}monetaryMarket.html?buyerCurrencyId={cc}&sellerCurrencyId=0')
            seller = tree.xpath("//tr[2]//td[1]/a/text()")[0].strip()
            if seller != nick:
                try:
                    MM = tree.xpath("//tr[2]//td[3]/b")[0].text
                except:
                    MM = 0.1
                payload = {"id": IDs[i - 2].value, "rate": round(float(MM) - 0.0001, 4), "submit": "Edit"}
                edit_offer = await get_content(URL + "monetaryMarket.html?action=change", data=payload)
                print(edit_offer)
        except:
            break

if __name__ == "__main__":
    print(mm.__doc__)
    servers = input("Servers (separated by a comma): ")
    for server in servers.split(","):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            mm(server))
    input("Press any key to continue")

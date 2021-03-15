import asyncio

from login import get_content


async def buffs(server, buffs_names):
    """Buy and use buffs."""
    URL = f"https://{server}.e-sim.org/"

    results = []
    for buff_name in buffs_names.split(","):
        buff_name = buff_name.strip().upper()
        if buff_name == "VAC":
            buff_name = "EXTRA_VACATIONS"
        elif buff_name == "SPA":
            buff_name = "EXTRA_SPA"
        elif buff_name == "SEWER":
            buff_name = "SEWER_GUIDE"
        elif "STR" in buff_name:
            buff_name = "STEROIDS"
        actions = ("BUY", "USE")
        for Index, action in enumerate(actions):
            payload = {'itemType': buff_name, 'storageType': "SPECIAL_ITEM", 'action': action, "quantity": 1}
            if action == "USE":
                payload = {'item': buff_name, 'storageType': "SPECIAL_ITEM", 'action': action, 'submit': 'Use'}
            url = await get_content(URL + "storage.html", data=payload, login_first=not Index)
            results.append(f"{buff_name}: {url}\n")
            if "error" in str(url):
                results.append(f"No such buff ({buff_name})\n")
                continue
    print("".join(results))

if __name__ == "__main__":
    print(buffs.__doc__)
    server = input("Server: ")
    buffs_names = input("Which buffs would you like to buy&use (separate them with a comma)? ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(buffs(server, buffs_names))
    input("Press any key to continue")

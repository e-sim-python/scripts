import asyncio

from login import get_content


async def reshuffle_or_upgrade(server, action, eq_id_or_link, parameter):
    """
    Reshuffle/upgrade specific parameter.
    Parameter example: Increase chance to avoid damage by 7.08%
    If it's not working, you can try writing "first" or "last" as parameter.
    """
    if action.lower() not in ("reshuffle", "upgrade"):
        print(f"'action' parameter can be reshuffle/upgrade only (not{action})")
        return
    URL = f"https://{server}.e-sim.org/"

    ID = str(eq_id_or_link).replace(f"{URL}showEquipment.html?id=", "")  # link case
    LINK = f"{URL}showEquipment.html?id={ID}"
    tree = await get_content(LINK, login_first=True)
    eq = tree.xpath('//*[@id="esim-layout"]//div/div[4]/div/h4/text()')
    parameterId = tree.xpath('//*[@id="esim-layout"]//div/div[4]/div/h3/text()')
    if parameter in eq[0].replace("by  ", "by ") or parameter == "first":
        parameterId = parameterId[0].split("#")[1]
    elif parameter in eq[1].replace("by  ", "by ") or parameter == "last":
        parameterId = parameterId[1].split("#")[1]
    else:
        print(f"Did not find parameter {parameter} at {LINK}. Try copy & paste.")
        return
    payload = {'parameterId': parameterId, 'action': f"{action.upper()}_PARAMETER", "submit": action.capitalize()}
    url = await get_content(URL + "equipmentAction.html", data=payload)
    print(url)

if __name__ == "__main__":
    print(reshuffle_or_upgrade.__doc__)
    server = input("Server: ")
    action = input("Type reshuffle / upgrades: ")
    eq_id_or_link = input("EQ id or link: ")
    parameter = input("Parameter (we recommend to copy and paste, but you can also write first/last): ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        reshuffle_or_upgrade(server, action, eq_id_or_link, parameter))
    input("Press any key to continue")

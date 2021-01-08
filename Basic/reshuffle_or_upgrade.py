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
    eq = tree.xpath('//*[@id="esim-layout"]//div/text()')
    if parameter in eq[1] or parameter == "first":
        parameterId = int(ID) * 2
    elif parameter in eq[2] or parameter == "last":
        parameterId = int(ID) * 2 - 1
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

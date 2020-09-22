from login import login
from lxml.html import fromstring

def reshuffle_or_upgrade(server, action, eq_id_or_link, parameter, session=""):
    """
    Reshuffle/upgrade specific parameter.
    Parameter example: Increase chance to avoid damage by 7.08%
    If it's not working, you can try writing "first" or "last" as parameter.
    """
    if action.lower() not in ("reshuffle", "upgrade"):
        print(f"'action' parameter can be reshuffle/upgrade only (not{action})")
        return
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    ID = str(eq_id_or_link).replace(f"{URL}showEquipment.html?id=", "")  # link case
    LINK = f"{URL}showEquipment.html?id={ID}"
    showEquipment = session.get(LINK)
    tree = fromstring(showEquipment.content)
    eq = tree.xpath('//*[@id="esim-layout"]//div/text()')
    if parameter in eq[1] or parameter == "first":
        parameterId = int(ID) * 2
    elif parameter in eq[2] or parameter == "last":
        parameterId = int(ID) * 2 - 1
    else:
        print(f"Did not find parameter {parameter} at {LINK}. Try copy & paste.")
        return
    payload = {'parameterId': parameterId, 'action': f"{action.upper()}_PARAMETER", "submit": action.capitalize()}
    send_action = session.post(URL + "equipmentAction.html", data=payload)
    print(send_action.url)
    return session


if __name__ == "__main__":
    print(reshuffle_or_upgrade.__doc__)
    server = input("Server: ")
    action = input("Type reshuffle / upgrades: ")
    eq_id_or_link = input("EQ id or link: ")
    parameter = input("Parameter (we recommend to copy and paste, but you can also write first/last): ")
    reshuffle_or_upgrade(server, action, eq_id_or_link, parameter)
    input("Press any key to continue")

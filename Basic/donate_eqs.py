from login import login

def donate_eqs(server, ids, receiver_id, session=""):
    """
    Donating specific EQ ID(s) to specific user.
    If you need anything else (gold, products) use contract (see accept_contract function)
    """
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    results = []
    for ID in ids.split(","):
        payload = {"equipmentId": ID.strip(), "id": receiver_id, "reason": " ", "submit": "Donate"}
        send_eq = session.post(URL + "donateEquipment.html", data=payload)
        results.append(f"ID {ID} - {send_eq.url}\n")
    print("".join(results))
    return session


if __name__ == "__main__":
    print(donate_eqs.__doc__)
    server = input("Server: ")
    ids = input("EQs ids (separated by a comma): ")
    receiver_id = input("Receiver citizen id: ")
    donate_eqs(server, ids, receiver_id)
    input("Press any key to continue")

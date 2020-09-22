from login import login

def accept_contract(server, contract_id, session=""):
    """Accept specific contract id."""
    if not session:
        session = login(server)
    payload = {'action': "ACCEPT", "id": contract_id, "submit": "Accept"}
    accept = session.post(f"https://{server}.e-sim.org/contract.html", data=payload)
    print(accept.url)
    return session


if __name__ == "__main__":
    print(accept_contract.__doc__)
    server = input("Server: ")
    contract_id = input("Contract id: ")
    accept_contract(server, contract_id)
    input("Press any key to continue")

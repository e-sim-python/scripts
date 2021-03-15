import asyncio

from login import get_content


async def accept_contract(server, contract_id):
    """Accept specific contract id."""
    payload = {'action': "ACCEPT", "id": contract_id, "submit": "Accept"}
    url = await get_content(f"https://{server}.e-sim.org/contract.html", data=payload, login_first=True)
    print(url)


if __name__ == "__main__":
    print(accept_contract.__doc__)
    server = input("Server: ")
    contract_id = input("Contract id: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(accept_contract(server, contract_id))
    input("Press any key to continue")

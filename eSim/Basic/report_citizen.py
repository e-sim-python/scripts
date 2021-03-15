import asyncio

from login import get_content


async def report(server, target_id, report_reason):
    """Reporting a citizen"""
    URL = f"https://{server}.e-sim.org/"

    payload = {"id": target_id, 'action': "REPORT_MULTI", "text": report_reason, "submit": "Submit"}
    url = await get_content(f"{URL}ticket.html", data=payload, login_first=True)
    print(url)

if __name__ == "__main__":
    print(report.__doc__)
    server = input("Server: ")
    target_id = input("Target citizen id: ")
    report_reason = input("Report reason: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        report(server, target_id, report_reason))
    input("Press any key to continue")

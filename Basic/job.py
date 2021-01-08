import asyncio

from login import double_click, get_content


async def job(server):
    """Leaving job and apply for the best offer at the local market."""
    URL = f"https://{server}.e-sim.org/"

    await get_content(URL + "work.html", data={'action': "leave", "submit": "Submit"}, login_first=True)
    tree = await get_content(URL + "jobMarket.html")
    jobId = tree.xpath("//tr[2]//td[6]//input[1]")[0].value
    url = await get_content(URL + "jobMarket.html", data={"id": jobId, "submit": "Apply"})
    print(url)
    await double_click(server)

if __name__ == "__main__":
    print(job.__doc__)
    server = input("Server: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        job(server))
    input("Press any key to continue")

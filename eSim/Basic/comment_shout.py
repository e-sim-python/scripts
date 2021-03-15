import asyncio

from login import get_content


async def comment_shout(server, shout_id, comment_body):
    URL = f"https://{server}.e-sim.org/"

    url = await get_content(f"{URL}replyToShout.html?id={shout_id}",
                            data={"body": comment_body, "submit": "Shout!"}, login_first=True)
    print(url)

if __name__ == "__main__":
    print(comment_shout.__doc__)
    server = input("Server: ")
    shout_id = input("Shout id (you can use F12): ")
    comment_body = input("Comment body: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        comment_shout(server, shout_id, comment_body))
    input("Press any key to continue")

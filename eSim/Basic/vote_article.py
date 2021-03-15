import asyncio

from login import get_content


async def article(server, article_id):
    """Voting an article"""
    URL = f"https://{server}.e-sim.org/"
    await get_content(f"{URL}vote.html", data={"id": article_id}, login_first=True)
    print(f"Voted article {article_id} at {server}")

if __name__ == "__main__":
    print(article.__doc__)
    server = input("Server: ")
    article_id = int(input("Article id or link: ").split("article.html?id=")[-1])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        article(server, article_id))
    input("Press any key to continue")

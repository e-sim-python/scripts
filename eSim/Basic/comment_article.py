import asyncio

from login import get_content


async def comment_article(server, article_id, comment_body):
    """Commenting an article"""
    URL = f"https://{server}.e-sim.org/"

    payload = {"action": "NEW", "key": f"Article {article_id}", "submit": "Publish", "body": comment_body}
    url = await get_content(URL + "comment.html", data=payload, login_first=True)
    print(url)

if __name__ == "__main__":
    print(comment_article.__doc__)
    server = input("Server: ")
    article_id = input("Article id: ")
    comment_body = input("Comment body: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        comment_article(server, article_id, comment_body))
    input("Press any key to continue")

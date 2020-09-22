from login import login

def comment_article(server, article_id, comment_body, session=""):
    """Commenting to an article"""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)    
    payload = {"action": "NEW", "key": f"Article {article_id}", "submit": "Publish", "body": comment_body}
    comment = session.post(URL + "comment.html", data=payload)
    print(comment.url)
    return session


if __name__ == "__main__":
    print(comment_article.__doc__)
    server = input("Server: ")
    article_id = input("Article id: ")
    comment_body = input("Comment body: ")
    comment_article(server, article_id, comment_body)
    input("Press any key to continue")

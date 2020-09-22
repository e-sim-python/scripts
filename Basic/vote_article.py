from login import login

def article(server, articleId, session=""):
    """Voting an article"""
    URL = f"https://{server}.e-sim.org/"
    articleId = str(articleId).replace(f"{URL}article.html?id=", "")
    if not session:
        session = login(server)
    session.post(f"{URL}vote.html?id={articleId}")
    print(f"Voted article {articleId} at {server}")
    return session

    
if __name__ == "__main__":
    print(article.__doc__)
    server = input("Server: ")
    articleId = input("Article id or link: ")
    article(server, articleId)
    input("Press any key to continue")

from login import login, double_click
from lxml.html import fromstring

def job(server, session=""):
    """Leaving job and apply for the best offer at the local market."""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    session.post(URL + "work.html", data={'action': "leave", "submit": "Submit"})
    jobMarket = session.get(URL + "jobMarket.html")
    tree = fromstring(jobMarket.content)
    jobId = tree.xpath("//tr[2]//td[6]//input[1]")[0].value
    apply = session.post(URL + "jobMarket.html", data={"id": jobId, "submit": "Apply"})
    print(apply.url)
    double_click(server, session=session)
    return session


if __name__ == "__main__":
    print(job.__doc__)
    server = input("Server: ")
    job(server)
    input("Press any key to continue")

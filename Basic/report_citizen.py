from login import login

def report(server, target_id, report_reason, session=""):
    """Reporting a citizen"""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    payload = {"id": target_id, 'action': "REPORT_MULTI", "text": report_reason, "submit": "Submit"}
    send_report = session.post(f"{URL}ticket.html", data=payload)
    print(send_report.url)
    return session


if __name__ == "__main__":
    print(report.__doc__)
    server = input("Server: ")
    target_id = input("Target citizen id: ")
    report_reason = input("Report reason: ")
    report(server, target_id, report_reason)
    input("Press any key to continue")

from login import login

from random import choice

def citizenship_or_mu_application(server, country_or_mu_id, action="cs", session=""):
    """Send application to MU / country."""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)

    messages = ["The application will be reviewed by congress members", "Hi ............... Accept me ..",
                "Coming to help you guys pls accept me",
                "[currency]GOLD[/currency][currency]GOLD[/currency]",
                "[citizen][citizen] [citizen][citizen] [/citizen][/citizen]",
                # feel free to add more at the same format: "item1", "item2"
                ]

    if action.lower() in ("citizenship", "cs"):
        payload = {'action': "APPLY", 'countryId': country_or_mu_id, "message": choice(messages),
                   "submit": "Apply for citizenship"}
        link = "citizenshipApplicationAction.html"
    else:
        payload = {'action': "SEND_APPLICATION", 'id': country_or_mu_id, "message": choice(messages),
                   "submit": "Send application"}
        link = "militaryUnitsActions.html"
        link2 = "myMilitaryUnit"
        # If there's already pending application
        session.post(URL + link2,  data={"action": "CANCEL_APPLICATION", "submit": "Cancel application"})

    send_application = session.post(URL + link, data=payload)
    print(send_application.url)
    return session


if __name__ == "__main__":
    print(citizenship_or_mu_application.__doc__)
    server = input("Server: ")
    action = input("Send to MU / CS: ")
    country_or_mu_id = input(f"{action} id: ")    
    citizenship_or_mu_application(server, country_or_mu_id, action)
    input("Press any key to continue")

import asyncio
from random import choice

from login import get_content

messages = ["The application will be reviewed by congress members", "Hi ............... Accept me ..",
            "Coming to help you guys pls accept me",
            "[currency]GOLD[/currency][currency]GOLD[/currency]",
            "[citizen][citizen] [citizen][citizen] [/citizen][/citizen]",
            # feel free to add more at the same format: "item1", "item2"
            ]


async def citizenship_or_mu_application(server, country_or_mu_id, action="cs"):
    """Send application to MU / country."""
    URL = f"https://{server}.e-sim.org/"

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
        await get_content(URL + link2,  data={"action": "CANCEL_APPLICATION", "submit": "Cancel application"},
                          login_first=True)

    url = await get_content(URL + link, data=payload, login_first="citizenship" in link)
    print(url)

if __name__ == "__main__":
    print(citizenship_or_mu_application.__doc__)
    server = input("Server: ")
    action = input("Send to MU / CS: ")
    country_or_mu_id = input(f"{action} id: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        citizenship_or_mu_application(server, country_or_mu_id, action))
    input("Press any key to continue")

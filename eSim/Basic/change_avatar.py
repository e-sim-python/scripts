import asyncio
import base64
from io import BytesIO

from aiohttp import ClientSession

from login import get_content


async def avatar(server, imgURL="https://source.unsplash.com/random/150x150"):
    """Change avatar img."""
    URL = f"https://{server}.e-sim.org/"
    async with ClientSession() as session:
        async with session.get(imgURL.strip()) as resp:
            avatarBase64 = str(base64.b64encode((BytesIO(await resp.read())).read()))[2:-1]

    payload = {"action": "CONTINUE", "v": f"data:image/png;base64,{avatarBase64}",
               "h": "none", "e": "none", "b": "none", "a": "none", "c": "none", "z": 1, "r": 0,
               "hh": 1, "eh": 1, "bh": 1, "ah": 1, "hv": 1, "ev": 1, "bv": 1, "av": 1, "act": ""}
    url = await get_content(URL + "editAvatar.html", data=payload, login_first=True)
    print(url)

if __name__ == "__main__":
    print(avatar.__doc__)
    server = input("Server: ")
    imgURL = input("Image url (example https://source.unsplash.com/random/150x150 ): ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        avatar(server, imgURL))
    input("Press any key to continue")

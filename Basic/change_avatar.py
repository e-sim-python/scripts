from login import login

import requests
from PIL import Image
from io import BytesIO
import base64

def avatar(server, imgURL="https://source.unsplash.com/random", session=""):
    """Change avatar img."""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    img = Image.open(BytesIO(requests.get(imgURL).content)).resize((150, 150), Image.ANTIALIAS)
    imgByteArr = BytesIO()
    img.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    avatarBase64 = str(base64.b64encode(imgByteArr))[2:-1]
    payload = {"action": "CONTINUE", "v": f"data:image/png;base64,{avatarBase64}",
               "h": "none", "e": "none", "b": "none", "a": "none", "c": "none", "z": 1, "r": 0,
               "hh": 1, "eh": 1, "bh": 1, "ah": 1, "hv": 1, "ev": 1, "bv": 1, "av": 1, "act": ""}
    edit_avatar = session.post(URL + "editAvatar.html", data=payload)
    print(edit_avatar.url)
    return session


if __name__ == "__main__":
    print(avatar.__doc__)
    server = input("Server: ")
    imgURL = input("Image url (example https://source.unsplash.com/random ): ")
    avatar(server, imgURL)
    input("Press any key to continue")

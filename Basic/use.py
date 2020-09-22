from login import login

def use(server, food_or_gift, quality="5", session=""):
    """Using food or gift"""
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)
    if food_or_gift.lower() == "food":
        food_or_gift = "eat"
    post_use = session.post(f"{URL}{food_or_gift}.html?quality={quality}")
    print(post_use.url)
    return session


if __name__ == "__main__":
    print(use.__doc__)
    server = input("Server: ")
    food_or_gift = input("Food / Gift: ")
    quality = input("Quality: ")
    use(server, food_or_gift, quality)
    input("Press any key to continue")

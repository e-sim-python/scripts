def imports():
    """Try importing most required modules for this library"""
    try:
        import requests
    except ImportError as packet:
        install([packet.name])
    try:
        import lxml
    except ImportError as packet:
        install([packet.name])

def install(packets):
    import subprocess
    for packet in packets:
        try:
            subprocess.call(['pip', 'install', packet.strip()])
        except Exception as e:
            print(e)
            input("Press any key to continue")


if __name__ == "__main__":
    imports()
    packets = input("Pls write the packets names you want to install (separated by a comma):\n").split(",")
    install(packets)
    input("The program is over. You may close this window now.")

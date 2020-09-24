input("This program should help you install lxml and requests modules, using many different methods. Press Enter to continue.")
try:
    from pip._internal import main
    main(['install', "lxml"])
    main(['install', "requests"])
    import lxml
    import requests
except:
    try:
        import pip
        pip.main(['install', "lxml"])
        pip.main(['install', "requests"])
        import lxml
        import requests

    except:
        try:
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", "lxml"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
            import lxml
            import requests                
        except:
            try:
                import subprocess
                subprocess.call(['pip', 'install', "lxml"])
                subprocess.call(['pip', 'install', "requests"])
                import lxml
                import requests   
            except Exception as e:
                print(e)
                print("Sorry, but i couldn't help. search in google for more options (your goal is to install requests and lxml modules")
                print("Here's a good place to start: https://www.google.com/search?q=Installing+python+module+within+code ")
                break
input("Press any key to continue")

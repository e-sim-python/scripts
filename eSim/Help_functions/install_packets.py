input("This program should help you install lxml and requests modules, using many different methods. Press Enter to continue.")


def method1(package):
    from pip._internal import main
    main(['install', package])
    import aiohttp
    import lxml
    

def method2(package):
    import pip
    pip.main(['install', package])
    import aiohttp
    import lxml


def method3(package):
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    import aiohttp
    import lxml


def method4(package):
    import subprocess
    subprocess.call(['pip', 'install', package])
    import aiohttp
    import lxml
    

for package in ["aiohttp", "lxml"]:
    try:
        method1(package)
    except:
        try:
            method2(package)
        except:
            try:
                method3(package)
            except:
                try:
                    method4(package)
                except Exception as e:
                    print(e)
                    print("Sorry, but i couldn't help. search in google for more options (your goal is to install requests and lxml modules")
                    print("Here's a good place to start: https://www.google.com/search?q=Installing+python+module+within+code ")
                    
input("Press any key to continue")

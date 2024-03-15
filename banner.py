from pyfiglet import figlet_format
from colorama import Fore, Style

def banner():  
    try:
        banner = figlet_format("ODINsec", font="slant")
        print(Fore.BLUE + banner + Style.RESET_ALL)
    except NameError:
        pass

import subprocess
import sys
from colorama import Fore, Style

def check_requirements():
    with open('requirements.txt', 'r') as file:
        required_packages = [line.strip() for line in file]

    missing_packages = []
    for package in required_packages:
        try:
            subprocess.check_output([sys.executable, '-m', 'pip', 'show', package], stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            missing_packages.append(package)
            
    if missing_packages:
        print(f"{Fore.RED}Error{Style.RESET_ALL}, the following required packages are missing: {', '.join(missing_packages)}.\nYou can install them using '{Fore.YELLOW}pip install -r requirements.txt{Style.RESET_ALL}'.")
        exit(1)

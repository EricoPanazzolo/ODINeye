import os
import logging
import subprocess
import sys
import shutil

"""Check if the required packages are installed"""
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


try:
    from pyfiglet import figlet_format 
    from colorama import Fore, Style
except ImportError:
    check_requirements()

"""Check if the required tools are installed"""
def check_tools_dependencies():
    required_tools = ['subfinder', 'haktrails', 'assetfinder', 'httpx', 'nuclei', 'nmap']

    missing_tools = []
    for tool in required_tools:
        if shutil.which(tool) is None:
            missing_tools.append(tool)

    if missing_tools:
        print(f"{Fore.RED}Error{Style.RESET_ALL}, the following required tools are missing: {Fore.YELLOW}{', '.join(missing_tools)}{Style.RESET_ALL}.")
        exit(1)

"""Prints the ODINsec banner"""
def banner():  
    try:
        banner = figlet_format("ODINeye", font="slant")
        print(Fore.BLUE + banner + Style.RESET_ALL)
    except NameError:
        pass

"""Prompts the user to enter a domain and returns it"""
def get_domain():
    domain = input("Enter the domain: ")
    return domain

"""Runs Subfinder tool"""
def run_subfinder(domain):
    return os.system(f"subfinder -d {domain} -o subf.txt -v")

"""Runs Haktrails tool"""
def run_haktrails(domain):
    return os.system(f'echo "{domain}" | haktrails subdomains > haksubs.txt')

"""Runs Assetfinder tool"""
def run_assetfinder(domain):
    return os.system(f"assetfinder -subs-only {domain} > asset.txt")

"""Organizes the subdomains into a single file"""
def organize_subdomains(domain):
    return os.system(f"cat subf.txt haksubs.txt asset.txt | sort -u > subdomains-{domain}.txt")

"""Runs HTTPX tool"""
def run_httpx(domain):
    return os.system(f"httpx -l subdomains-{domain}.txt -o active-subdomains-{domain}.txt -threads 200 -status-code -follow-redirects")

"""Runs Nuclei tool"""
def run_nuclei(domain):
    return os.system(f"nuclei -l subdomains-{domain}.txt -o nuclei-subdomains-{domain}.txt")

"""Runs Nmap tool"""
def run_nmap(domain):
    return os.system(f"nmap -sC -sV -A -iL subdomains-{domain}.txt -o nmap-subdomains-{domain}.txt")

"""Cleans up temporary files"""
def clean_up():
    return os.system("rm subf.txt haksubs.txt asset.txt")

"""Main function to execute the entire workflow"""
def main():
    logging.basicConfig(filename='odinsec.log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
    banner()
    check_tools_dependencies()
    domain = get_domain()
    try:
        run_subfinder(domain)
        run_haktrails(domain)
        run_assetfinder(domain)
        organize_subdomains(domain)
        run_httpx(domain)
        run_nuclei(domain)
        run_nmap(domain)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.error(f"Error running tool: {e}")
        print(f"Error running tool: {e}")
    finally:
        clean_up()

if __name__ == "__main__":
    main()
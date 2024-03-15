import os
import shutil
from colorama import Fore, Style

def check_tools_dependencies():
    required_tools = ['subfinder', 'haktrails', 'assetfinder', 'httpx', 'nuclei', 'nmap']

    missing_tools = []
    for tool in required_tools:
        if shutil.which(tool) is None:
            missing_tools.append(tool)

    if missing_tools:
        print(f"{Fore.RED}Error{Style.RESET_ALL}, the following required tools are missing: {Fore.YELLOW}{', '.join(missing_tools)}{Style.RESET_ALL}.")
        exit(1)

def run_subfinder(domain):
    return os.system(f"subfinder -d {domain} -o subf.txt -v")

def run_haktrails(domain):
    return os.system(f'echo "{domain}" | haktrails subdomains > haksubs.txt')

def run_assetfinder(domain):
    return os.system(f"assetfinder -subs-only {domain} > asset.txt")

def organize_subdomains(domain):
    return os.system(f"cat subf.txt haksubs.txt asset.txt | sort -u > subdomains-{domain}.txt")

def run_httpx(domain):
    return os.system(f"httpx -l subdomains-{domain}.txt -o active-subdomains-{domain}.txt -threads 200 -status-code -follow-redirects")

def run_nuclei(domain):
    return os.system(f"nuclei -l subdomains-{domain}.txt -o nuclei-subdomains-{domain}.txt")

def run_nmap(domain):
    return os.system(f"nmap -sC -sV -A -iL subdomains-{domain}.txt -o nmap-subdomains-{domain}.txt")

def clean_up():
    return os.system("rm subf.txt haksubs.txt asset.txt")

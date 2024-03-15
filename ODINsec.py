import os
import subprocess
import logging

from pyfiglet import figlet_format

def banner():  
    print(figlet_format("ODINsec", font="slant"))

def get_domain():
    domain = input("Enter the domain: ")
    return domain

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

def main():
    logging.basicConfig(filename='odinsec.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    banner()
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

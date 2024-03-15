import os
import logging
# import pkg_resources
import subprocess
import sys

def check_requirements():
    with open('requirements.txt', 'r') as file:
        required_packages = [line.strip() for line in file]

    # Verificar quais bibliotecas estão faltando
    missing_packages = []
    for package in required_packages:
        try:
            subprocess.check_output([sys.executable, '-m', 'pip', 'show', package], stderr=subprocess.DEVNULL)
            print(f"Package {package} is installed.")
        except subprocess.CalledProcessError:
            missing_packages.append(package)

    # Se houver bibliotecas faltando, exibir mensagem de erro
    if missing_packages:
        print(f"Error: The following required packages are missing: {', '.join(missing_packages)}.\nYou can install them using 'pip install -r requirements.txt'.")
        exit(1)

try:
    from pyfiglet import figlet_format 
except ImportError:
    check_requirements()

def banner():  
    try:
        print(figlet_format("ODINsec", font="slant"))
    except NameError:
        pass

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
    logging.basicConfig(filename='odinsec.log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
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

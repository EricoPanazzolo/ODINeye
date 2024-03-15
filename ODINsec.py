import os
import logging
import subprocess
import sys
import shutil
from colorama import Fore, Style
from banner import banner
from tools import check_tools_dependencies, run_subfinder, run_haktrails, run_assetfinder, organize_subdomains, run_httpx, run_nuclei, run_nmap, clean_up
from requirements import check_requirements

def main():
    logging.basicConfig(filename='odinsec.log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
    banner()
    check_requirements()
    check_tools_dependencies()
    domain = input("Enter the domain: ")
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

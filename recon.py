#!/usr/bin/env python3
# KENZ RECON SUITE - Educational Purpose Only
# Author: KENZ a.k.a JARVIS
import requests
import dns.resolver
from colorama import Fore, Style, init
import sys
import time

# Inisialisasi warna
init(autoreset=True)

class KenzRecon:
    def __init__(self, target_domain):
        self.target = target_domain
        self.subdomains = ['www', 'mail', 'ftp', 'dev', 'admin', 'test', 'staging', 'api', 'vpn', 'secure']
        self.admin_paths = ['/admin', '/login', '/wp-admin', '/admin.php', '/login.php', '/console', '/dashboard']
        self.headers = {'User-Agent': 'Mozilla/5.0 (KenzRecon/1.0)'}

    def print_banner(self):
        print(Fore.CYAN + f"""
        [+] TARGET: {self.target}
        [+] MODE: Active Reconnaissance
        [+] MODULES: Dorking, Subdomain, Admin Finder
        """)

    def google_dorking(self):
        print(Fore.YELLOW + "[*] Generating Google Dorks (Manual Check Required)...")
        # [span_6](start_span)Teknik Passive Reconnaissance[span_6](end_span)
        dorks = [
            f"site:{self.target} ext:pdfOr ext:docOr ext:docx",
            f"site:{self.target} inurl:admin",
            f"site:{self.target} inurl:login",
            f"site:{self.target} intitle:index.of",
            f"site:{self.target} intext:\"password\" filetype:log"
        ]
        for dork in dorks:
            query = dork.replace(' ', '+')
            print(f"    [>] https://www.google.com/search?q={query}")
        print(Fore.GREEN + "[+] Dork links generated.\n")

    def enum_subdomains(self):
        print(Fore.YELLOW + "[*] Starting Subdomain Discovery (DNS Brute Force)...")
        # [span_7](start_span)Teknik Active Enumeration[span_7](end_span)
        found = []
        for sub in self.subdomains:
            hostname = f"{sub}.{self.target}"
            try:
                answers = dns.resolver.resolve(hostname, 'A')
                for rdata in answers:
                    print(Fore.GREEN + f"    [+] FOUND: {hostname} -> {rdata.address}")
                    found.append(hostname)
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
                pass
        if not found:
            print(Fore.RED + "    [-] No common subdomains found.")
        else:
            print(Fore.GREEN + f"[+] Discovery finished. Found {len(found)} subdomains.\n")

    def find_admin_login(self):
        print(Fore.YELLOW + "[*] Hunting Admin & Login Panels...")
        # [span_8](start_span)Teknik Directory Discovery / Exposed Panels[span_8](end_span)
        found = False
        for path in self.admin_paths:
            url = f"http://{self.target}{path}"
            try:
                res = requests.get(url, headers=self.headers, timeout=5)
                if res.status_code == 200:
                    print(Fore.GREEN + f"    [!!!] EXPOSED PANEL: {url} (Status: 200)")
                    found = True
                elif res.status_code in [301, 302, 403]:
                    print(Fore.BLUE + f"    [!] INTERESTING: {url} (Status: {res.status_code})")
            except requests.exceptions.RequestException:
                pass
        
        if not found:
            print(Fore.RED + "    [-] No obvious admin panels found in common paths.")
        print("\n")

if __name__ == "__main__":
    try:
        target = input("Enter Target Domain (e.g., example.com): ")
        if not target:
            sys.exit("Target required!")
            
        scanner = KenzRecon(target)
        scanner.print_banner()
        
        # Phase 1: Dorking
        scanner.google_dorking()
        
        # Phase 2: Subdomain Enum
        scanner.enum_subdomains()
        
        # Phase 3: Admin Finder
        scanner.find_admin_login()
        
        print(Fore.CYAN + "[*] Scan Complete. Happy Hacking.")
        
    except KeyboardInterrupt:
        print("\n[!] Aborted by user.")

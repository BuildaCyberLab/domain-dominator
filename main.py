import requests
import dns.resolver
import json
from concurrent.futures import ThreadPoolExecutor
from prettytable import PrettyTable
import os

# Vulnerable services with detection logic
VULNERABLE_SERVICES = {
    'amazonaws.com': "AWS S3 bucket may be unclaimed.",
    'herokuapp.com': "Heroku app may be unclaimed.",
    'github.io': "GitHub Pages may be unclaimed.",
    'cloudfront.net': "CloudFront distribution may be unclaimed.",
    'azurewebsites.net': "Azure website may be unclaimed.",
    'unbouncepages.com': "Unbounce page may be unclaimed.",
}

# Subdomain enumeration function
def enumerate_subdomains(domain):
    """
    Enumerates subdomains using crt.sh and other public sources.
    """
    print(f"[*] Enumerating subdomains for {domain}...")
    subdomains = set()

    # crt.sh enumeration
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for cert in data:
                subdomains.add(cert['name_value'])
    except Exception as e:
        print(f"  [!] Error fetching subdomains from crt.sh: {e}")

    # Add additional methods for enumeration here (e.g., APIs, brute-forcing)

    print(f"  [+] Found {len(subdomains)} subdomains.")
    return list(subdomains)

# DNS resolution function
def resolve_dns(subdomain):
    """
    Resolves DNS records (CNAME) for a given subdomain.
    """
    try:
        answers = dns.resolver.resolve(subdomain, 'CNAME')
        for rdata in answers:
            return rdata.target.to_text().rstrip('.')
    except dns.resolver.NXDOMAIN:
        return None
    except Exception:
        return None

# Check for vulnerable services
def check_vulnerability(cname):
    """
    Checks if a CNAME points to a vulnerable service.
    """
    for service, message in VULNERABLE_SERVICES.items():
        if service in cname:
            return message
    return None

# Validate HTTP responses
def validate_http(subdomain):
    """
    Validates if a subdomain is live via HTTP requests.
    """
    try:
        response = requests.head(f"http://{subdomain}", timeout=5)
        return response.status_code < 400
    except requests.exceptions.RequestException:
        return False

# Main scanning function
def scan_subdomain(subdomain):
    """
    Scans a single subdomain for vulnerabilities.
    """
    print(f"[*] Scanning {subdomain}...")
    cname = resolve_dns(subdomain)
    if not cname:
        print(f"  [-] No CNAME record found for {subdomain}.")
        return None

    print(f"  [+] CNAME: {cname}")
    vulnerability = check_vulnerability(cname)
    if vulnerability:
        print(f"  [!] Vulnerability detected: {vulnerability}")
        return {"subdomain": subdomain, "cname": cname, "issue": vulnerability}

    # Optional: Check if the subdomain is live
    if validate_http(subdomain):
        print(f"  [+] {subdomain} is live.")
    else:
        print(f"  [-] {subdomain} is not live.")

    return None

# Generate a report
def generate_report(results, output_file="report.json"):
    """
    Generates a JSON report of findings.
    """
    print(f"\n[*] Generating report...")
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)
    print(f"  [+] Report saved to {output_file}.")

# Main function
def main():
    # User input
    domain = input("Enter the target domain (e.g., example.com): ").strip()

    # Enumerate subdomains
    subdomains = enumerate_subdomains(domain)

    # Scan subdomains for vulnerabilities
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for result in executor.map(scan_subdomain, subdomains):
            if result:
                results.append(result)

    # Output results
    if results:
        print("\n[!] Vulnerabilities detected:")
        table = PrettyTable(["Subdomain", "CNAME", "Issue"])
        for entry in results:
            table.add_row([entry['subdomain'], entry['cname'], entry['issue']])
        print(table)

        # Generate a report
        generate_report(results)
    else:
        print("\n[+] No vulnerabilities detected.")

if __name__ == "__main__":
    main()

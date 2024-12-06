# **Domain Dominator**  
**Uncover. Dominate. Secure.**  

**Domain Dominator** is a powerful Python tool for advanced subdomain enumeration and vulnerability detection. It resolves DNS records, maps services, and identifies misconfigurations that could lead to subdomain takeovers, such as unclaimed AWS S3 buckets or GitHub Pages. Lightweight, fast, and open-source, it’s designed for penetration testers, bug bounty hunters, and cybersecurity professionals.  

---

## **Features**  
- **Subdomain Enumeration:** Discover subdomains using public sources like `crt.sh`.  
- **DNS Resolution:** Map DNS records (CNAME, A) to identify associated services.  
- **Takeover Detection:** Detect vulnerabilities in services like AWS S3, Heroku, Azure, etc.  
- **HTTP Validation:** Check if subdomains are live and serving content.  
- **Actionable Reports:** Generate clean JSON reports for analysis.  

---

## **Installation**  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/domain-dominator.git
   cd domain-dominator
   ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

---

## **Usage**  
Run the tool with a target domain:  
```bash
python main.py --domain example.com --output report.json
```

**Example Output:**  
```
[*] Enumerating subdomains for example.com...
[+] Found 10 subdomains.
[*] Scanning sub.vulnerable.example.com...
[!] Vulnerability detected: AWS S3 bucket may be unclaimed.

[!] Vulnerabilities detected:
  Subdomain: sub.vulnerable.example.com
  CNAME: unclaimed.s3.amazonaws.com
  Issue: AWS S3 bucket may be unclaimed.
```

**JSON Report Example:**  
```json
[
    {
        "subdomain": "sub.vulnerable.example.com",
        "cname": "unclaimed.s3.amazonaws.com",
        "issue": "AWS S3 bucket may be unclaimed."
    }
]
```

---

## **Contributing**  
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.  

---

## **License**  
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  

---

## **Disclaimer**  
This tool is intended for educational and authorized security testing purposes only. Unauthorized use is prohibited.  

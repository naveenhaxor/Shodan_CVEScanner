import shodan
import pandas as pd

# Define the path to your text file with IP addresses
file_path = 'ENTER_FILE.TXT'

# Your Shodan API key
SHODAN_API_KEY = 'ENTER_SHODAN_API_KEY'

# Initialize the Shodan API
api = shodan.Shodan(SHODAN_API_KEY)

def get_vulnerabilities(ip):
    try:
        # Lookup the IP
        host = api.host(ip)
        
        # Extract and return CVE vulnerabilities
        vulnerabilities = host.get('vulns', [])
        return vulnerabilities
    except shodan.APIError as e:
        print(f"Error fetching data for {ip}: {e}")
        return []

def main():
    try:
        with open(file_path, 'r') as file:
            ips = file.read().splitlines()
        
        data = []
        
        for ip in ips:
            vulnerabilities = get_vulnerabilities(ip)
            if vulnerabilities:
                cve_details = ", ".join(vulnerabilities)
                data.append({'Vulnerable IP Address': ip, 'CVE Details': f"{ip} ({cve_details})"})
            else:
                data.append({'Vulnerable IP Address': ip, 'CVE Details': f"{ip} (No CVE found or error occurred)"})
        
        # Create a DataFrame
        df = pd.DataFrame(data)
        
        # Save the DataFrame to an Excel file
        df.to_excel('shodan_vulnerabilities.xlsx', index=False)
        
        print("Data saved to shodan_vulnerabilities.xlsx")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()

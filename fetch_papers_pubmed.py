import requests
from bs4 import BeautifulSoup
import json
import csv
import re

def fetch_pubmed_data(pubmed_id):
    url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"
    response = requests.get(url)
    
    # Ensure the request was successful
    if response.status_code != 200:
        return {"error": "Failed to fetch the article"}

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extracting necessary details from the page
    try:
        title = soup.find("h1", class_="heading-title").get_text(strip=True)
        publication_date = soup.find("span", class_="cit").get_text(strip=True)
        authors = [author.get_text(strip=True) for author in soup.find_all("a", class_="full-name")]
        
        # Look for email addresses using mailto links
        email = "N/A"
        email_link = soup.find("a", href=re.compile(r"^mailto:"))
        if email_link:
            email = email_link.get("href").replace("mailto:", "")
        
        company_affiliation = "N/A"  # Company affiliations might not be directly available
        
        # Output the results in a dictionary
        output = {
            'PubmedID': pubmed_id,
            'Title': title,
            'Publication Date': publication_date,
            'Authors': ", ".join(authors) if authors else "N/A",
            'Non-academic Author(s)': "N/A",  # This might need manual inspection
            'Company Affiliation(s)': company_affiliation,
            'Corresponding Author Email': email
        }

    except Exception as e:
        output = {"error": f"Failed to extract data: {str(e)}"}

    return output

def save_to_csv(data, filename):
    # Define the header for the CSV file
    header = ['PubmedID', 'Title', 'Publication Date', 'Authors', 'Non-academic Author(s)', 'Company Affiliation(s)', 'Corresponding Author Email']
    
    # Open CSV file in write mode
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    pubmed_ids = ["40075025", "40075026", "40075027", "40075028", "40075029"]  # Replace with actual PubMed IDs
    papers_data = []

    # Fetch data for each PubMed ID
    for pubmed_id in pubmed_ids:
        paper_data = fetch_pubmed_data(pubmed_id)
        papers_data.append(paper_data)

    # Display the data in the console
    for paper in papers_data:
        print(json.dumps(paper, indent=4))

    # Save the data to a CSV file
    save_to_csv(papers_data, 'pubmed_papers.csv')
    print("\nData has been saved to 'pubmed_papers.csv'")

# Run the main function
if __name__ == "__main__":
    main()

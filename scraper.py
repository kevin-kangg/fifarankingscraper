import requests
from bs4 import BeautifulSoup
import csv
import argparse

def scrape_transfermarkt_world_ranking(date, limit=None):
    base_url = f"https://www.transfermarkt.us/statistik/weltrangliste/statistik/stat/datum/{date}/plus/0/galerie/0/page/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        data = []
        page = 1
        while True:
            url = f"{base_url}{page}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the rankings table
            rankings_table = soup.find('table', class_='items')
            if rankings_table:
                # Extract rows from the table
                rows = rankings_table.find_all('tr')
                for row in rows:
                    # Extract columns from each row
                    columns = row.find_all('td')
                    # Ensure the row has at least 3 columns
                    if len(columns) >= 3:
                        if date == "2024-04-04":
                            rank = columns[0].text.strip()
                            nation = columns[1].text.strip()
                            confederation = columns[5].text.strip()
                            points = columns[6].text.strip()
                        else:
                            rank = columns[0].text.strip()
                            nation = columns[1].text.strip()
                            confederation = columns[2].text.strip()
                            points = columns[3].text.strip()
                        data.append((rank, nation, confederation, points, date))
                        # Check if the limit is reached
                        if limit and len(data) >= limit:
                            return data
                # Check if there exists more pages
                next_page_link = soup.find('a', class_='tm-pagination__link', title='Go to the next page')
                if not next_page_link:
                    # Exit loop if no more pages
                    break
                page += 1
            else:
                print("Rankings table not found.")
                return None
        return data
    except requests.exceptions.RequestException as e:
        print("Failed to fetch the page:", e)
        return None

def print_data(data):
    for entry in data:
        print(entry)

def main():
    parser = argparse.ArgumentParser(description="Scrape FIFA World Rankings data")
    parser.add_argument('--scrape', type=int, help="Number of dates to scrape")
    parser.add_argument('--save', metavar='filename', help="Save scraped data to a CSV file")

    args = parser.parse_args()

    if args.scrape is not None and args.scrape <= 0:
        print("Invalid value for --scrape argument. Please provide a positive integer.")
        return

    all_data = []

    url = "https://www.transfermarkt.us/statistik/weltrangliste/statistik/stat/plus/0/galerie/0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find dropdown menu containing dates
        date_select = soup.find('select', attrs={'name': 'datum'})
        if date_select:
            # Extract date options
            date_options = date_select.find_all('option')[:args.scrape] if args.scrape else date_select.find_all('option')
            for option in date_options:
                date_value = option.get('value')
                print(f"Scraping data for {option.text}...")
                scraped_data = scrape_transfermarkt_world_ranking(date_value)
                if scraped_data:
                    all_data.extend(scraped_data)
                else:
                    print("No rankings data found.")
        
        if args.save:
            with open(args.save, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Rank', 'Nation', 'Confederation', 'Points', 'Date'])
                writer.writerows(all_data)
            print(f"All data saved to {args.save}")
        else:
            print_data(all_data)
    except requests.exceptions.RequestException as e:
        print("Failed to fetch the page:", e)

if __name__ == "__main__":
    main()

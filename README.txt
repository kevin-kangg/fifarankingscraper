FIFA World Rankings Scraper

This script allows you to scrape FIFA World Rankings data from the Transfermarkt website. You can choose to scrape a specific number of dates and either print the data to standard output or save it to a CSV file.

Usage:
1. scraper.py
   - The script invocation without input arguments prints the complete scraped dataset as rows of data to standard output.
   
2. scraper.py --scrape N
   - The script invocation with the flag --scrape N scrapes only the first N entries of the dataset and prints them to standard output.
   
3. scraper.py --save <path_to_dataset>
   - This script invocation saves the complete scraped dataset into the file passed as input.

Sample Invocations:
- `scraper.py --scrape 10` - Scrapes the data for the first 10 dates and prints them to standard output.
- `scraper.py --save my_scraped_data.csv` - Scrapes the complete dataset and saves it to a CSV file named my_scraped_data.csv.
- `scraper.py --scrape 5 --save my_data.csv` - Scrapes the data for the first 5 dates and saves them to a CSV file named my_data.csv.

Instructions:
1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Run the script using one of the sample invocations mentioned above.

Note: Make sure to replace `<path_to_dataset>` with the desired path for saving the CSV file.


import pandas as pd  # Importing the pandas library for data manipulation.
import requests  # Importing the requests library for making HTTP requests.
from bs4 import BeautifulSoup  # Importing BeautifulSoup for HTML parsing.
import re  # Importing the re module for regular expressions.

def scrape_links():
    """
    Scrapes property links from multiple pages on a website "Zameen.com".
    """

    all_links = []  # Defining "all_links" variable to initialize an empty list to store the links.

    page = 1  # Defining "page" variable as 1 to start scraping from page 1.

    while True:  # Using WHILE LOOP to continue scraping until there are no more listings on the page

        print(f'Scraping Page no {page}')  # Print the current page number being scraped to whatch the progress

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36',
            'Connection': 'keep-alive'
        }  # Set headers to mimic a web browser

        url = f'https://www.zameen.com/Homes/Karachi-2-{page}.html'  # Base URL of the web page to scrape

        response = requests.get(url, headers=headers)  # Send a GET request to the URL

        soup = BeautifulSoup(response.content, 'html.parser')  # Create a BeautifulSoup object

        listings = soup.find_all('li', class_='ef447dde')  # Find all listings on the page

        if not listings:  # If there are no listings (means that there are no pages left to scrape), break the loop 
            break
        
        # Iterate over each listing element to scrape the links.
        for listing in listings:  
            link = listing.find('a')['href']  # Extract the link from the listing element
            link = 'https://www.zameen.com' + link  # Append the base URL to the link

            if not listing:  # If the listing is empty, skip to the next iteration
                pass

            # Check if the link already exists in the list
            if link not in all_links:
                all_links.append(link)  # Add the link to the list of all links

        page += 1  # Move to the next page

    # Create a DataFrame with the links
    df = pd.DataFrame({'links': all_links})

    # Save the DataFrame to a CSV file
    df.to_csv('links.csv', index=False)

    return all_links


def scrape_info():
    """
    Scrapes the information using the links obtained from scrape_links function.
    """

    links = pd.read_csv('links.csv')  # Read the links from the CSV file.
    link_list = links['links']  # Get the list of links from the DataFrame.
    info = []  # Initialize an empty list to store the scraped information.
    listing_num = 1 # Initialize the listing number counter.

    # Set headers to mimic a web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36',
        'Connection': 'keep-alive'
    } 
    
    # Iterate over each link.
    for link in link_list:  
        response = requests.get(link, headers=headers)  # Send a GET request to the link
        soup = BeautifulSoup(response.content, 'html.parser')  # Create a BeautifulSoup object
        page = soup.find('ul', class_='_033281ab')  # Find the page element containing the property information

        if not page:  # If the page element is not found, skip to the next iteration
            continue

        page = page.text  # Get the text content of the page element

        # Extract property information using regular expressions
        property_type = re.search(r'Type(.*?)Price', page)
        property_type = property_type.group(1).strip() if property_type else ""

        property_price = re.search(r'Price(.*?)Location', page)
        property_price = property_price.group(1).strip() if property_price else ""

        property_location = re.search(r'Location(.*?)Bath', page)
        property_location = property_location.group(1).strip() if property_location else ""

        bed = re.search(r'Bedroom\(s\)(.*?)Added', page)
        bed = bed.group(1).strip() if bed else ""

        bath = re.search(r'Bath\(s\)(.*?)Area', page)
        bath = bath.group(1).strip() if bath else ""

        property_area = re.search(r'Area(.*?)Purpose', page)
        property_area = property_area.group(1).strip() if property_area else ""

        property_description = soup.find('span', class_='_2a806e1e').text.strip()  # Find the property description element and extract the text

        property_link = link  # Store the link

        print(listing_num)  # Print the listing number to watch the progress.

        # Append the scraped information to the list
        info.append({
            'Type': property_type,
            'Price': property_price,
            'Location': property_location,
            'No of Beds': bed,
            'No of Baths': bath,
            'Area in Sq. yd.': property_area,
            'Description': property_description,
            'Web link': property_link
        })

        listing_num += 1  # Increment the listing number

    df = pd.DataFrame(info)  # Create a DataFrame with the scraped information
    df.to_csv('scraped_info.csv', index=False)  # Save the DataFrame to a CSV file

    return info


if __name__ == '__main__':
    scrape_links()  # Call the scrape_links function to scrape the property links
    scrape_info()  # Call the scrape_info function to scrape the property information

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def scrap_info():
    links = pd.read_csv('properties_link.csv')
    link_list = links['links']
    info = []
    listing_num = 1  # Move the initialization here

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36',
        'Connection': 'keep-alive'
    }

    for link in link_list:
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        page = soup.find('ul', class_='_033281ab')

        if not page:
            continue
        
        page = soup.find('ul', class_='_033281ab').text

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

        property_description = soup.find('span', class_='_2a806e1e').text.strip()

        property_link = link

        print(listing_num)

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
        listing_num += 1

    df = pd.DataFrame(info)
    df.to_csv('scraped_info.csv', index=False)

    return info

if __name__ == '__main__':
    scrap_info()

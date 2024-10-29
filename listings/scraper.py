# listings/scraper.py
import requests
from bs4 import BeautifulSoup
from .models import Listing

def fetch_listings_from_olx(city, max_price):
    print("intra")
    url = f"https://www.olx.ro/imobiliare/apartamente-garsoniere-de-vanzare/{city.lower()}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    listings = []

    for item in soup.select('.offer-wrapper'):
        title = item.select_one('.lheight22.margintop5 a').get_text().strip()
        price_text = item.select_one('.price strong').get_text().strip().replace(" ", "")
        price = float(price_text.replace("EUR", "").replace(",", "."))
        link = item.select_one('.lheight22.margintop5 a')['href']
        date_posted = item.select_one('.bottom-cell .color-9').get_text().strip()

        if price <= max_price:
            listings.append(
                Listing(
                    title=title,
                    price=price,
                    city=city,
                    url=link,
                    date_posted=date_posted
                )
            )
    return listings

def fetch_all_listings(city, max_price):
    all_listings = []
    all_listings.extend(fetch_listings_from_olx(city, max_price))
    # Poți adăuga alte funcții de scraping aici
    return all_listings

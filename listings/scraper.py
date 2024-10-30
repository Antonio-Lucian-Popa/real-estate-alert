# listings/scraper.py
import requests
from bs4 import BeautifulSoup
from .models import Listing
import datetime


def fetch_listings_from_olx(city, max_price):
    print("Incepem scraping-ul")
    url = f"https://www.olx.ro/imobiliare/apartamente-garsoniere-de-vanzare/{city.lower()}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    listings = []

    # Selectăm fiecare element de anunț pe baza structurii HTML furnizate
    for item in soup.select('div.css-qfzx1y'):
        # Extragem titlul
        title_tag = item.select_one('h6.css-1wxaaza')
        title = title_tag.get_text().strip() if title_tag else "Titlu necunoscut"
        print(f"Titlu extras: {title}")  # Mesaj de debug pentru a verifica titlul extras

        # Extragem prețul
        price_tag = item.select_one('p[data-testid="ad-price"]')
        price_text = price_tag.get_text().strip().replace(" ", "") if price_tag else "0"
        try:
            price = float(price_text.replace("€", "").replace(",", "."))
        except ValueError:
            print("Preț necunoscut sau format invalid")  # Mesaj de debug pentru preț
            continue  # Dacă prețul nu poate fi convertit, trecem la următorul anunț
        print(f"Preț extras: {price}")  # Mesaj de debug pentru a verifica prețul extras

        # Extragem link-ul
        link_tag = item.select_one('a.css-z3gu2d')
        link = link_tag['href'] if link_tag else "#"
        print(f"Link extras: {link}")  # Mesaj de debug pentru a verifica link-ul extras

        # Extragem data și locația
        date_location_tag = item.select_one('p[data-testid="location-date"]')
        date_posted_text = date_location_tag.get_text().strip() if date_location_tag else None

        # Verificăm și convertim data postării într-un format corect
        if date_posted_text:
            try:
                # Încearcă să parsezi data (în funcție de formatul site-ului)
                date_posted = datetime.datetime.strptime(date_posted_text, "%d %B %Y")
            except ValueError:
                # Dacă data nu poate fi interpretată, folosim data curentă
                date_posted = datetime.datetime.now()
        else:
            # Dacă nu există dată, folosim data curentă
            date_posted = datetime.datetime.now()

        print(f"Data postării extrasă: {date_posted}")  # Mesaj de debug pentru data postării

        # Filtrăm listările după prețul maxim
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
    print(f"Numărul total de anunțuri extrase: {len(listings)}")  # Mesaj de debug pentru numărul de anunțuri extrase
    return listings


def fetch_all_listings(city, max_price):
    all_listings = []
    all_listings.extend(fetch_listings_from_olx(city, max_price))
    # Poți adăuga alte funcții de scraping aici
    return all_listings

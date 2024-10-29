# listings/tasks.py
from celery import shared_task
from .scraper import fetch_all_listings
from .models import Listing, SearchPreference

@shared_task
def check_for_new_listings():
    preference = SearchPreference.objects.first()
    if preference:
        city = preference.city
        max_price = preference.max_price
        listings = fetch_all_listings(city, max_price)

        for listing in listings:
            Listing.objects.get_or_create(
                title=listing.title,
                price=listing.price,
                city=listing.city,
                url=listing.url,
                date_posted=listing.date_posted
            )

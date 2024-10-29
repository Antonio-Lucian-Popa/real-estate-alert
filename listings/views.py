from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Listing
from .serializers import ListingSerializer
from .scraper import fetch_listings_from_olx  # Importă funcția de scraping


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class FilteredListingsView(APIView):
    def get(self, request, *args, **kwargs):
        city = request.query_params.get('city', None)
        max_price = request.query_params.get('max_price', None)

        # Verificăm că parametrii au fost trimiși
        if city is None or max_price is None:
            return Response({"error": "Please provide both 'city' and 'max_price' parameters."}, status=400)

        try:
            max_price = float(max_price)  # Convertim prețul la număr pentru a filtra
        except ValueError:
            return Response({"error": "'max_price' must be a number."}, status=400)

        # Filtrăm listările după oraș și preț maxim
        listings = Listing.objects.filter(city__iexact=city, price__lte=max_price)

        # Dacă nu există listări, apelăm funcția de scraping pentru a obține listări noi
        if not listings.exists():
            new_listings = fetch_listings_from_olx(city, max_price)

            # Salvăm listările noi în baza de date
            for listing in new_listings:
                Listing.objects.get_or_create(
                    title=listing.title,
                    price=listing.price,
                    city=city,
                    url=listing.url,
                    date_posted=listing.date_posted
                )

            # Reîncărcăm listările după ce au fost salvate
            listings = Listing.objects.filter(city__iexact=city, price__lte=max_price)

        # Serializăm și returnăm rezultatele
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)

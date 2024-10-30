from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Listing
from .serializers import ListingSerializer
from .scraper import fetch_listings_from_olx  # Importă funcția de scraping
from .models import SearchPreference
from .serializers import SearchPreferenceSerializer

from real_estate_alert.scheduler import scrape_job
import logging


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class FilteredListingsView(APIView):
    def get(self, request, *args, **kwargs):
        city = request.query_params.get('city', None)
        max_price = request.query_params.get('max_price', None)

        # Validăm că prețul maxim este un număr
        try:
            max_price = float(max_price)
        except ValueError:
            return Response({"error": "'max_price' must be a number."}, status=400)

        # 1. Căutăm listările existente în baza de date
        listings = Listing.objects.filter(city__iexact=city, price__lte=max_price)

        # 2. Facem scraping pentru a obține listări noi
        new_listings = fetch_listings_from_olx(city, max_price)
        for listing in new_listings:
            # Verifică dacă există deja în baza de date pe baza URL-ului
            if not Listing.objects.filter(url=listing.url).exists():
                Listing.objects.create(
                    title=listing.title,
                    price=listing.price,
                    city=city,
                    url=listing.url,
                    date_posted=listing.date_posted
                )

        # 3. Reîncărcăm listările după ce au fost salvate, pentru a include și cele noi
        all_listings = Listing.objects.filter(city__iexact=city, price__lte=max_price)

        # Serializăm și returnăm toate listările (atât cele din baza de date, cât și cele noi)
        serializer = ListingSerializer(all_listings, many=True)
        return Response(serializer.data)


class SearchPreferenceView(APIView):
    def get(self, request):
        # Returnăm preferințele curente
        preference = SearchPreference.objects.first()
        if preference:
            serializer = SearchPreferenceSerializer(preference)
            return Response(serializer.data)
        return Response({"detail": "No preferences set."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Creăm sau actualizăm preferințele
        data = request.data
        preference, created = SearchPreference.objects.update_or_create(
            id=1,  # folosim ID-ul 1 pentru o singură preferință globală
            defaults={
                "city": data.get("city"),
                "max_price": data.get("max_price"),
            }
        )
        return Response(SearchPreferenceSerializer(preference).data, status=status.HTTP_200_OK)


class ScrapeJobAPIView(APIView):
    def get(self, request):
        try:
            scrape_job()  # Apelează funcția de scraping
            return Response({"message": "Scraping job completed successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"Error during scraping job: {e}")
            return Response({"error": "Scraping job failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

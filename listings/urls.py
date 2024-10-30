# listings/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, FilteredListingsView
from .views import SearchPreferenceView
from .views import ScrapeJobAPIView


router = DefaultRouter()
router.register(r'listings', ListingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('filtered_listings/', FilteredListingsView.as_view(), name='filtered_listings'),
    path('search-preferences/', SearchPreferenceView.as_view(), name='search-preferences'),
    path('trigger-scrape/', ScrapeJobAPIView.as_view(), name='trigger-scrape'),
]

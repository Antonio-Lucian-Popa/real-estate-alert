# listings/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, FilteredListingsView

router = DefaultRouter()
router.register(r'listings', ListingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('filtered_listings/', FilteredListingsView.as_view(), name='filtered_listings'),
]

# listings/serializers.py
from rest_framework import serializers
from .models import Listing
from .models import SearchPreference

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'


class SearchPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchPreference
        fields = ['city', 'max_price']

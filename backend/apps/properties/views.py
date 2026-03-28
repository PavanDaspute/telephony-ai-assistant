"""
DRF views for the Properties API.
"""

from rest_framework import generics, filters
from .models import Property
from .serializers import PropertySerializer


class PropertyListView(generics.ListAPIView):
    """
    GET /api/properties/
    Returns a paginated list of all properties.
    Supports search via ?search=<term> on title, location, description.
    """

    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "location", "description"]
    ordering_fields = ["price", "bedrooms", "carpet_area", "created_at"]
    ordering = ["-created_at"]


class PropertyDetailView(generics.RetrieveAPIView):
    """
    GET /api/properties/<id>/
    Returns details for a single property.
    """

    queryset = Property.objects.all()
    serializer_class = PropertySerializer

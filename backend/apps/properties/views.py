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

    # ⚡ Performance Optimization: fetch only required fields to reduce DB load
    # 🚫 N+1 Avoidance Note: If any ForeignKey or ManyToMany fields are added to Property
    # in the future, remember to chain .select_related('fk_field') or .prefetch_related('m2m_field')
    queryset = Property.objects.all().only(
        "id", "title", "location", "price", "carpet_area", "bedrooms"
    )
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

    # ⚡ Performance Optimization: fetch only required fields for detail view
    queryset = Property.objects.all().only(
        "id", "title", "location", "price", "carpet_area", 
        "bedrooms", "amenities", "description"
    )
    serializer_class = PropertySerializer

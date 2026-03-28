"""
DRF serializers for the Property model.
"""

from rest_framework import serializers
from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    """
    Serializes all public fields of a property listing.
    Includes a computed `price_in_lakhs` field for human-readable display.
    """

    price_in_lakhs = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            "id",
            "title",
            "location",
            "price",
            "price_in_lakhs",
            "carpet_area",
            "bedrooms",
            "amenities",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "price_in_lakhs"]

    def get_price_in_lakhs(self, obj: Property) -> str:
        """Return price formatted as 'X lakh'."""
        return obj.price_in_lakhs()

"""
Property model representing a real estate listing.
"""

from django.db import models


class Property(models.Model):
    """
    Represents a real estate property/flat with all relevant details.
    """

    title = models.CharField(max_length=255, db_index=True, help_text="Short title for the property")
    location = models.CharField(max_length=255, db_index=True, help_text="Area/city where the property is located")
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        db_index=True,
        help_text="Price in INR (e.g. 7500000 for 75 lakh)",
    )
    carpet_area = models.PositiveIntegerField(help_text="Carpet area in square feet")
    bedrooms = models.PositiveSmallIntegerField(help_text="Number of bedrooms (BHK)")
    amenities = models.JSONField(
        default=list,
        blank=True,
        help_text="List of amenities, e.g. ['swimming pool', 'gym', 'parking']",
    )
    description = models.TextField(blank=True, help_text="Detailed description of the property")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ["-created_at"]
        # Added composite index to optimize queries filtering by both location and price
        indexes = [
            models.Index(fields=["location", "price"]),
        ]

    def __str__(self):
        return f"{self.title} — {self.location}"

    def price_in_lakhs(self) -> str:
        """Return a human-friendly price string in lakhs."""
        lakhs = self.price / 100_000
        if lakhs == int(lakhs):
            return f"{int(lakhs)} lakh"
        return f"{lakhs:.1f} lakh"

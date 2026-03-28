"""
Management command to seed sample property data for development/testing.

Usage:
    python manage.py seed_properties
"""

from django.core.management.base import BaseCommand
from apps.properties.models import Property


SAMPLE_PROPERTIES = [
    {
        "title": "Luxury 2BHK in Wakad",
        "location": "Wakad, Pune",
        "price": 7500000,  # 75 lakh
        "carpet_area": 850,
        "bedrooms": 2,
        "amenities": ["swimming pool", "gym", "covered parking", "24/7 security", "power backup"],
        "description": (
            "A beautiful 2BHK apartment in the heart of Wakad with modern amenities. "
            "Close to IT parks, schools, and shopping centres. Ready to move in."
        ),
    },
    {
        "title": "Spacious 3BHK in Baner",
        "location": "Baner, Pune",
        "price": 12000000,  # 1.2 crore
        "carpet_area": 1200,
        "bedrooms": 3,
        "amenities": ["rooftop garden", "gym", "clubhouse", "2 parking slots", "children's play area"],
        "description": (
            "A premium 3BHK flat in Baner offering panoramic views and world-class amenities. "
            "Ideal for families. Well connected to Balewadi and Aundh."
        ),
    },
    {
        "title": "Affordable 1BHK in Hinjewadi",
        "location": "Hinjewadi, Pune",
        "price": 4200000,  # 42 lakh
        "carpet_area": 520,
        "bedrooms": 1,
        "amenities": ["lift", "gated community", "visitor parking", "CCTV surveillance"],
        "description": (
            "Smart 1BHK apartment perfect for IT professionals working in Hinjewadi Phase 1 & 2. "
            "Excellent connectivity and affordable pricing."
        ),
    },
]


class Command(BaseCommand):
    help = "Seeds the database with sample property listings."

    def handle(self, *args, **options):
        created_count = 0
        for data in SAMPLE_PROPERTIES:
            obj, created = Property.objects.get_or_create(
                title=data["title"],
                defaults=data,
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  Created: {obj}'))
            else:
                self.stdout.write(f'  Already exists: {obj}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {created_count} new properties seeded.'
        ))

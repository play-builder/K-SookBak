from django.core.management.base import BaseCommand
from rooms.models                import Facility

class Command(BaseCommand):

    help = "This command creates facilities"

    def handle(self, *args, **opetions):
        facilities = [
            "Private entrance",
            "Paid Parking on Premises",
            "Paid parking off Premises",
            "Elevator",
            "Parking",
            "Gym"
        ]
        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} Facilities created!"))

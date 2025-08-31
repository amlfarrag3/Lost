from django.core.management.base import BaseCommand
from finder.models import MissingPerson, Searcher, Report
from django.contrib.auth.models import User
from datetime import date

class Command(BaseCommand):
    help = "Seed database with sample data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        # Create sample users
        user1, _ = User.objects.get_or_create(username="john_doe", defaults={"email": "john@example.com"})
        user2, _ = User.objects.get_or_create(username="jane_smith", defaults={"email": "jane@example.com"})

        # Create searchers
        searcher1, _ = Searcher.objects.get_or_create(
            user=user1,
            defaults={
                "full_name": "John Doe",
                "phone_number": "123456789",
                "email": "john@example.com"
            }
        )

        searcher2, _ = Searcher.objects.get_or_create(
            user=user2,
            defaults={
                "full_name": "Jane Smith",
                "phone_number": "987654321",
                "email": "jane@example.com"
            }
        )

        # Create missing persons
        person1, _ = MissingPerson.objects.get_or_create(
            full_name="Ali Hassan",
            date_of_birth=date(2010, 5, 12),
            gender="M",
            blood_type="A+",
            disappearance_location="Cairo",
            disappearance_date=date(2023, 10, 15),
            photo="missing_persons_photos/ali.jpg"
        )

        person2, _ = MissingPerson.objects.get_or_create(
            full_name="Sara Mohamed",
            date_of_birth=date(2008, 3, 22),
            gender="F",
            blood_type="O-",
            disappearance_location="Giza",
            disappearance_date=date(2024, 1, 5),
            photo="missing_persons_photos/sara.jpg"
        )

        # Create reports
        Report.objects.get_or_create(
            missing_person=person1,
            searcher=searcher1,
            defaults={"status": "Active"}
        )

        Report.objects.get_or_create(
            missing_person=person2,
            searcher=searcher2,
            defaults={"status": "Active"}
        )

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully!"))

from django.core.management.base import BaseCommand
from finder.models import MissingPerson, Searcher, Report
from django.core.files.uploadedfile import SimpleUploadedFile
import random
from datetime import date, timedelta

# Static test data
NAMES = ["Ahmed Mohamed", "Fatima Ali", "Youssef Khaled", "Mariam Saeed", "Ali Hassan", "Nour Mohamed", "Omar Gamal", "Laila Fouad", "Mostafa Ibrahim", "Heba Galal"]
SEARCHER_NAMES = ["Khaled Gamal", "Marwa Adel", "Hassan Tarek", "Dina Samir", "Mahmoud Kamal"]
GENDERS = ['M', 'F']
BLOOD_TYPES = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
LOCATIONS = ["Cairo", "Alexandria", "Assiut", "Minya", "Fayoum"]

class Command(BaseCommand):
    help = 'Seeds the database with sample data for development.'

    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        MissingPerson.objects.all().delete()
        Searcher.objects.all().delete()
        Report.objects.all().delete()
        
        self.stdout.write("Creating new sample data...")

        # Create Missing Persons
        for i in range(10):
            name = NAMES[i]
            gender = random.choice(GENDERS)
            blood_type = random.choice(BLOOD_TYPES)
            location = random.choice(LOCATIONS)
            
            random_age = random.randint(5, 45)
            birth_date = date.today() - timedelta(days=random_age * 365)
            dummy_photo = SimpleUploadedFile(f"photo_{i}.jpg", b"file_content", content_type="image/jpeg")

            MissingPerson.objects.create(
                full_name=name,
                date_of_birth=birth_date,
                gender=gender,
                blood_type=blood_type,
                disappearance_location=location,
                disappearance_date=date.today(),
                photo=dummy_photo
            )
        self.stdout.write(self.style.SUCCESS('Successfully created 10 missing persons!'))

        # Create Searchers
        for name in SEARCHER_NAMES:
            Searcher.objects.create(
                full_name=name,
                phone_number=f"0100{random.randint(1000000, 9999999)}",
                email=f"{name.replace(' ', '').lower()}@example.com"
            )
        self.stdout.write(self.style.SUCCESS('Successfully created 5 searchers!'))

        # Create Reports
        all_missing_persons = MissingPerson.objects.all()
        all_searchers = Searcher.objects.all()

        for _ in range(15):
            missing_person = random.choice(all_missing_persons)
            searcher = random.choice(all_searchers)

            Report.objects.create(
                missing_person=missing_person,
                searcher=searcher
            )
        self.stdout.write(self.style.SUCCESS('Successfully created 15 reports!'))

        self.stdout.write(self.style.SUCCESS('Database has been seeded!'))
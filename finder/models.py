from django.db import models


class MissingPerson(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES, null=True, blank=True)
    mother_blood_type=models.CharField(max_length=3,choices=BLOOD_TYPES,null=True,blank=True)
    father_blood_type=models.CharField(max_length=3,choices=BLOOD_TYPES,null=True,blank=True)
    disappearance_location = models.CharField(max_length=200)
    disappearance_date = models.DateField()
    photo = models.ImageField(upload_to='missing_persons_photos/')

    def __str__(self) ->(str) :
        return self.full_name # to view missing persons on admin page by their full name
    
    class Meta:
        ordering=['-disappearance_date'] # to view missing persons ordered by newer 

class Searcher(models.Model):
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self) ->(str) :
        return self.full_name 
    
    class Meta:
        ordering=['-created_at']


class Report(models.Model):
    missing_person = models.ForeignKey(MissingPerson, on_delete=models.CASCADE)
    searcher = models.ForeignKey(Searcher, on_delete=models.CASCADE)
    report_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Active')

    def __str__(self):
        return f"Report for {self.missing_person.full_name} by {self.searcher.full_name}"

from django import forms
from .models import Report
from .models import MissingPerson

class MissingPersonForm(forms.ModelForm):
    class Meta:
        model = MissingPerson
        fields = [
            "full_name", "gender", "date_of_birth", "blood_type",
            "disappearance_date", "disappearance_location", "photo",
            "mother_blood_type", "father_blood_type"
        ]

BLOOD_TYPES = [
    ('', '--- Select---'),
    ('O+', 'O+'), ('O-', 'O-'),
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
]

class AdvancedSearchForm(forms.Form):
    name = forms.CharField(required=False, label="Name")
    address = forms.CharField(required=False, label="Address")
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Missing Date From")
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='TO')
    
    blood_type = forms.ChoiceField(choices=BLOOD_TYPES, required=False, label="Blood Type")
    mother_blood_type = forms.ChoiceField(choices=BLOOD_TYPES, required=False, label="Mother Blood Type")
    father_blood_type = forms.ChoiceField(choices=BLOOD_TYPES, required=False, label="Father Blood Type")


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["status"]  


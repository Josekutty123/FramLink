import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'framelink.settings')
import django
django.setup()

from django.contrib.auth.hashers import make_password
from myapp.models import InsuranceOfficer

def create_officer():
    email = "alex@gmail.com"
    if not InsuranceOfficer.objects.filter(email=email).exists():
        officer = InsuranceOfficer(
            full_name="Alex",
            email=email,
            password=make_password("alex@50"),
            role="INSURANCE_OFFICER"
        )
        officer.save()
        print("Insurance Officer created successfully.")
    else:
        print("Insurance Officer already exists.")

create_officer()

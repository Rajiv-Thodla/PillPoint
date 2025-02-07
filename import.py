import os
import json
from django.db import IntegrityError
from main.models import Medicine, Symptom  # Import models

# Define common symptoms to extract
SYMPTOM_LIST = ["headache", "fever", "cough", "hypertension", "diabetes", "pain", "inflammation", "nausea", "vomiting"]

def extract_symptoms(text):
    """Find known symptoms in the indications text."""
    if text:
        return [symptom for symptom in SYMPTOM_LIST if symptom in text.lower()]
    return []

def import_medicines_from_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                data = json.load(file)

            for entry in data.get("results", []):
                try:
                    # Safely extract fields, using "Unknown" if missing
                    name = entry.get("openfda", {}).get("brand_name", ["Unknown"])[0]
                    description = entry.get("description", [""])[0]
                    indications = entry.get("indications_and_usage", [""])[0]
                    manufacturer = entry.get("openfda", {}).get("manufacturer_name", ["Unknown"])[0]
                    ndc_code = entry.get("openfda", {}).get("product_ndc", [""])[0]

                    # Avoid duplicate entries
                    medicine, created = Medicine.objects.get_or_create(
                        name=name,
                        ndc_code=ndc_code,
                        defaults={
                            "description": description,
                            "indications": indications,
                            "manufacturer": manufacturer,
                        }
                    )

                    # If it's a new medicine, extract and add symptoms
                    if created:
                        found_symptoms = extract_symptoms(indications)
                        for symptom_name in found_symptoms:
                            symptom, _ = Symptom.objects.get_or_create(name=symptom_name)
                            medicine.symptoms.add(symptom)

                except IntegrityError:
                    print(f"Skipping duplicate medicine: {name}")
                except Exception as e:
                    print(f"Error importing from {filename}: {e}")

# Run the import
import_medicines_from_folder("C:\\Users\\wib\\Downloads\\devjam bs")

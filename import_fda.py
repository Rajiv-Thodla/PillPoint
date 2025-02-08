import os
import json
import gdown
from django.db import IntegrityError
from main.models import Medicine, Symptom

DRIVE_FOLDER_URL = "https://drive.google.com/drive/folders/1XL_vOfcpSoUmc5ZkGmImgBARB4HH4G-C?usp=drive_link"
DEST_FOLDER = "fda_data"
SYMPTOM_LIST = ["headache", "fever", "cough", "hypertension", "diabetes", "pain", "inflammation", "nausea", "vomiting"]

def extract_symptoms(text):
    if text:
        return [symptom for symptom in SYMPTOM_LIST if symptom in text.lower()]
    return []

def download_fda_files():
    if not os.path.exists(DEST_FOLDER):
        os.makedirs(DEST_FOLDER)
    print("Downloading FDA data files from Google Drive folder...")
    downloaded_files = gdown.download_folder(url=DRIVE_FOLDER_URL, output=DEST_FOLDER, quiet=False)
    print("Download complete.")
    return downloaded_files

def import_medicines_from_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {file_path}")
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {filename}: {e}")
                continue
            for entry in data.get("results", []):
                try:
                    openfda = entry.get("openfda", {})
                    name = openfda.get("brand_name", ["Unknown"])[0]
                    manufacturer = openfda.get("manufacturer_name", ["Unknown"])[0]
                    indications = entry.get("indications_and_usage", [""])[0]
                    description = entry.get("description", [""])[0] if entry.get("description") else ""
                    ndc_code = openfda.get("product_ndc", [""])[0]
                    medicine, created = Medicine.objects.get_or_create(
                        name=name,
                        ndc_code=ndc_code,
                        defaults={
                            "description": description,
                            "indications": indications,
                            "manufacturer": manufacturer,
                        }
                    )
                    if created:
                        found_symptoms = extract_symptoms(indications)
                        for symptom_name in found_symptoms:
                            symptom, _ = Symptom.objects.get_or_create(name=symptom_name)
                            medicine.symptoms.add(symptom)
                        print(f"Imported medicine: {name}")
                    else:
                        print(f"Medicine already exists: {name}")
                except IntegrityError:
                    print(f"Skipping duplicate medicine: {name}")
                except Exception as e:
                    print(f"Error importing entry from {filename}: {e}")
    print("FDA medicine data import complete.")

if __name__ == "__main__":
    download_fda_files()
    import_medicines_from_folder(DEST_FOLDER)

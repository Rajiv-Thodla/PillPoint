from django.db import models

class Symptom(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    indications = models.TextField(null=True, blank=True)  # Conditions the medicine treats
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    ndc_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    symptoms = models.ManyToManyField(Symptom, blank=True)

    def __str__(self):
        return self.name

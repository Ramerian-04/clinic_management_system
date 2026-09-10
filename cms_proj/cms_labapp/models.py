from django.db import models

# Create your models here.
"""
labtech_app/models.py
Lab Technician's own module: FR-LAB-01 to FR-LAB-02.
Owns: LabTestResult. The lab test *order* lives in doctor_app.LabTest —
the Lab Technician reads that queue and writes results here.
"""

from cms_backendapp.models import generate_prefixed_id
from django.db import models, transaction


class LabTestResult(models.Model):
    result_id = models.CharField(max_length=15, primary_key=True)
    test = models.OneToOneField(
        "doctor_app.LabTest", on_delete=models.CASCADE, related_name="result"
    )
    performed_by = models.ForeignKey(
        "cms_backend.Staff", on_delete=models.PROTECT, related_name="lab_results_performed"
    )
    result_date = models.DateField()
    result_data = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lab_test_results"
        indexes = [models.Index(fields=["performed_by"])]

    def __str__(self):
        return f"Result for {self.test_id}"

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.result_id:
            self.result_id = generate_prefixed_id("LAB_RESULT", "LABR")
        super().save(*args, **kwargs)
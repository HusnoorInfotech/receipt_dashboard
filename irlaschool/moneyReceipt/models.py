
from django.db import models
from django.utils import timezone

import random
import string

def generate_receipt_no():
    # Generate a unique receipt number (e.g., 8 characters long)
    return ''.join(random.choices(string.digits, k=8))

# Create your models here.

class MoneyReceipt(models.Model):
    SECTION_CHOICES = [
        ('preprimary', 'Pre-Primary'),
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('college', 'College'),
    ]

    receipt_no = models.CharField(primary_key=True,default=generate_receipt_no, editable=False, unique=True)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    with_computers = models.BooleanField(default=False)
    student_name = models.CharField(max_length=100)
    standard = models.CharField(max_length=10)
    date = models.DateField(default=timezone.now)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Receipt No: {self.receipt_no} - {self.student_name}'

    class Meta:
        verbose_name = 'Money Receipt'
        verbose_name_plural = 'Money Receipts'

from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import MoneyReceipt   # Replace with your actual model name
import uuid
from django.utils import timezone
from datetime import timedelta
import random
from decimal import Decimal

class YourModelTestCase(TestCase):
    # Constants
    SECTIONS = ['preprimary', 'primary', 'secondary', 'college']
    STANDARDS = ['nursery','lkg','ukg','lkg','class 1', 'class 2', 'class 3', 'class 4', 'class 5', 'class 6', 'class 7', 'class 8', 'class 9', 'class 10', 'class 11', 'class 12']
    MIN_FEES = Decimal('100.00')
    MAX_FEES = Decimal('16000.00')
    NAMES = ["John", "Jane", "Robert", "Emily", "Michael", "Sarah", "David", "Jessica", "William", "Ashley"]

    @classmethod
    def setUpTestData(cls):
        cls.test_instances = []
        for _ in range(100):
            # Random data generation
            section = random.choice(cls.SECTIONS)
            with_computers = random.choice([True, False])
            student_first = random.choice(cls.NAMES)
            student_last = random.choice(cls.NAMES)
            student_name = f"{student_first} {student_last}"
            standard = random.choice(cls.STANDARDS)
            # Random date within ±1 year
            date = timezone.now() + timedelta(days=random.randint(-365, 365))
            total_fees = Decimal(random.uniform(float(cls.MIN_FEES), float(cls.MAX_FEES))).quantize(Decimal('0.01'))

            instance = MoneyReceipt.objects.create(
                section=section,
                with_computers=with_computers,
                student_name=student_name,
                standard=standard,
                date=date,
                total_fees=total_fees
            )
            cls.test_instances.append(instance)

    # Helper methods
    def assert_valid_uuid(self, uuid_string):
        try:
            uuid.UUID(str(uuid_string))
            return True
        except ValueError:
            return False

    # Test cases
    def test_receipt_no_generation(self):
        """Test that receipt_no is generated as a valid UUID"""
        for instance in self.test_instances:
            self.assertTrue(self.assert_valid_uuid(instance.receipt_no))
            self.assertIsInstance(instance.receipt_no, uuid.UUID)

    def test_section_choices(self):
        """Test all section choices are valid"""
        for instance in self.test_instances:
            self.assertIn(instance.section, dict(MoneyReceipt.SECTION_CHOICES))

    def test_with_computers_type(self):
        """Test with_computers field is boolean"""
        for instance in self.test_instances:
            self.assertIsInstance(instance.with_computers, bool)

    def test_student_name_length(self):
        """Test student_name length constraints"""
        for instance in self.test_instances:
            self.assertGreater(len(instance.student_name), 0)
            self.assertLessEqual(len(instance.student_name), 100)

    def test_standard_length(self):
        """Test standard length constraints"""
        for instance in self.test_instances:
            self.assertGreater(len(instance.standard), 0)
            self.assertLessEqual(len(instance.standard), 10)

    def test_date_range(self):
        """Test date is within expected range"""
        now = timezone.now()
        min_date = now - timedelta(days=365)
        max_date = now + timedelta(days=365)
        for instance in self.test_instances:
            self.assertGreaterEqual(instance.date, min_date)
            self.assertLessEqual(instance.date, max_date)

    def test_total_fees_range(self):
        """Test total_fees is within expected range"""
        for instance in self.test_instances:
            self.assertGreaterEqual(instance.total_fees, self.MIN_FEES)
            self.assertLessEqual(instance.total_fees, self.MAX_FEES)

    def test_model_string_representation(self):
        """Test __str__ method if exists"""
        if hasattr(MoneyReceipt, '__str__'):
            for instance in self.test_instances:
                self.assertIsInstance(str(instance), str)

    def test_unique_receipt_no(self):
        """Test receipt_no is unique across all instances"""
        receipt_nos = set()
        for instance in self.test_instances:
            self.assertNotIn(instance.receipt_no, receipt_nos)
            receipt_nos.add(instance.receipt_no)
    
    # Add more specific test cases as needed...
    # Total test methods will be much fewer than 100, but they collectively test
    # 100 different model instances with randomized data for comprehensive coverage

    def test_model_creation_count(self):
        """Verify we created exactly 100 test instances"""
        self.assertEqual(MoneyReceipt.objects.count(), 100)
        self.assertEqual(len(self.test_instances), 100)

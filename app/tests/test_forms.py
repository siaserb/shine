from django.core.exceptions import ValidationError
from django.test import TestCase

from app.forms import (
    RedactorCreateForm,
    RedactorUpdateForm,
    validate_years_of_experience,
)


class FormsTests(TestCase):
    def setUp(self):
        self.form_data_for_redactor = {
            "username": "sofia",
            "password1": "pass316321word",
            "password2": "pass316321word",
            "years_of_experience": 10,
            "first_name": "Sofia",
            "last_name": "Kisel",
        }

    def test_redactor_creation_form_with_valid_data(self):
        form = RedactorCreateForm(data=self.form_data_for_redactor)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data_for_redactor)

    def test_invalid_years_of_experience_during_creation(self):
        self.form_data_for_redactor["years_of_experience"] = 150
        form = RedactorCreateForm(data=self.form_data_for_redactor)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)

    def test_invalid_years_of_experience_during_update(self):
        print("Second")
        form = RedactorUpdateForm(data={"years_of_experience": 150})
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)


class ValidateYearsOfExperienceTest(TestCase):
    def test_valid_years_of_experience(self):
        self.assertEqual(validate_years_of_experience(10), 10)

    def test_invalid_years_of_experience(self):
        with self.assertRaises(ValidationError):
            validate_years_of_experience(150)

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password",
        )
        self.client.force_login(self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="redactor", password="password", years_of_experience="88"
        )

    def test_redactor_years_of_experience_listed(self):
        """
        Test that the license number displayed on redactor admin page.
        """
        url = reverse("admin:app_redactor_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.redactor.years_of_experience)

    def test_redactor_detail_years_of_experience_listed(self):
        """
        Test that the license number displayed on redactor`s detail admin page.
        """
        url = reverse("admin:app_redactor_change", args=[self.redactor.pk])
        response = self.client.get(url)
        self.assertContains(response, self.redactor.years_of_experience)

    def test_redactor_add_years_of_experience_field(self):
        """
        Test that the license number field is included in the add form.
        """
        url = reverse("admin:app_redactor_add")
        response = self.client.get(url)
        self.assertContains(response, "years_of_experience")

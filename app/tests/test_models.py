from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models import Topic, Newspaper


class RedactorModelTests(TestCase):

    def setUp(self):
        self.redactor = get_user_model().objects.create_user(
            username="test_username",
            password="password123",
            first_name="test_first_name",
            last_name="test_last_name",
            years_of_experience=5,
        )

    def test_redactor_str(self):
        self.assertEqual(
            str(self.redactor),
            f"{self.redactor.username} "
            f"({self.redactor.first_name} {self.redactor.last_name})",
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.redactor.get_absolute_url(), f"/redactors/{self.redactor.pk}/"
        )


class TopicModelTests(TestCase):

    def test_topic_str(self):
        topic = Topic.objects.create(name="test_topic")
        self.assertEqual(str(topic), "test_topic")


class NewspaperModelTests(TestCase):

    def setUp(self):
        self.topic = Topic.objects.create(name="test_topic")
        self.redactor = get_user_model().objects.create_user(
            username="test_username",
            password="password123",
            first_name="test_first_name",
            last_name="test_last_name",
            years_of_experience=5,
        )
        self.newspaper = Newspaper.objects.create(
            title="test_title",
            content="test_content",
        )
        self.newspaper.topics.add(self.topic)
        self.newspaper.publishers.add(self.redactor)

    def test_newspaper_str(self):
        self.assertEqual(str(self.newspaper), "test_title")

    def test_newspaper_topics_relationship(self):
        self.assertIn(self.topic, self.newspaper.topics.all())

    def test_newspaper_publishers_relationship(self):
        self.assertIn(self.redactor, self.newspaper.publishers.all())

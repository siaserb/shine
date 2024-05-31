from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app.forms import (
    TopicNameSearchForm,
    NewspaperTitleSearchForm,
    RedactorUsernameSearchForm,
)
from app.models import Topic, Newspaper

TOPIC_LIST_URL = reverse("app:topic-list")
NEWSPAPER_LIST_URL = reverse("app:newspaper-list")
REDACTOR_LIST_URL = reverse("app:redactor-list")


def get_topic_detail_url(pk):
    return reverse("app:topic-detail", args=[pk])


def get_newspaper_detail_url(pk):
    return reverse("app:newspaper-detail", args=[pk])


def get_redactor_detail_url(pk):
    return reverse("app:redactor-detail", args=[pk])


class PublicTopicTest(TestCase):
    def test_login_required(self):
        response = self.client.get(TOPIC_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTopicTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username",
            password="password",
        )
        self.client.force_login(self.user)
        Topic.objects.create(name="test_topic")
        Topic.objects.create(name="test_topic2")

    def test_retrieve_topics(self):
        response = self.client.get(TOPIC_LIST_URL)
        self.assertEqual(response.status_code, 200)
        topics = Topic.objects.all()
        self.assertEqual(list(response.context["topics"]), list(topics))
        self.assertTemplateUsed(response, "app/topic_list.html")

    def test_topic_search_form(self):
        response = self.client.get(TOPIC_LIST_URL, {"name": "test_topic"})
        form = TopicNameSearchForm(data={"name": "test_topic"})
        self.assertTrue(form.is_valid())
        self.assertContains(response, "test_topic")


class PublicNewspaperTest(TestCase):
    def test_login_required_for_list(self):
        response = self.client.get(NEWSPAPER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_detail(self):
        newspaper = Newspaper.objects.create(
            title="test_title",
            content="test_content"
        )
        response = self.client.get(get_newspaper_detail_url(newspaper.pk))
        self.assertNotEqual(response.status_code, 200)


class PrivateNewspaperTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username",
            password="password",
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="test_topic")
        self.newspaper = Newspaper.objects.create(
            title="test_title", content="test_content"
        )
        self.newspaper.topics.add(self.topic)

    def test_retrieve_newspapers(self):
        response = self.client.get(NEWSPAPER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        newspapers = Newspaper.objects.prefetch_related("topics")
        self.assertEqual(
            list(response.context["newspapers"]),
            list(newspapers)
        )
        self.assertTemplateUsed(response, "app/newspaper_list.html")

    def test_newspaper_detail_view(self):
        response = self.client.get(get_newspaper_detail_url(self.newspaper.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.newspaper.title)
        self.assertTemplateUsed(response, "app/newspaper_detail.html")

    def test_newspaper_search_form(self):
        response = self.client.get(NEWSPAPER_LIST_URL, {"title": "test_title"})
        form = NewspaperTitleSearchForm(data={"title": "test_title"})
        self.assertTrue(form.is_valid())
        self.assertContains(response, "test_title")


class PublicRedactorTest(TestCase):
    def test_login_required_for_list(self):
        response = self.client.get(REDACTOR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_detail(self):
        redactor = get_user_model().objects.create_user(
            username="redactor", password="password"
        )
        response = self.client.get(get_redactor_detail_url(redactor.pk))
        self.assertNotEqual(response.status_code, 200)


class PrivateRedactorTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username",
            password="password",
        )
        self.client.force_login(self.user)
        self.redactor = get_user_model().objects.create_user(
            username="redactor1",
            password="password123",
        )

    def test_retrieve_redactors(self):
        get_user_model().objects.create_user(
            username="redactor2",
            password="password123",
        )
        response = self.client.get(REDACTOR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        redactors = get_user_model().objects.all()
        self.assertEqual(list(response.context["redactors"]), list(redactors))
        self.assertTemplateUsed(response, "app/redactor_list.html")

    def test_create_redactor(self):
        form_data = {
            "username": "test_redactor",
            "password1": "pass1word123",
            "password2": "pass1word123",
            "first_name": "test_name",
            "last_name": "test_last_name",
        }
        self.client.post(reverse("app:redactor-create"), form_data)
        new_redactor = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(new_redactor.first_name, form_data["first_name"])
        self.assertEqual(new_redactor.last_name, form_data["last_name"])

    def test_redactor_detail_view(self):
        response = self.client.get(get_redactor_detail_url(self.redactor.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.redactor.username)
        self.assertTemplateUsed(response, "app/redactor_detail.html")

    def test_redactor_search_form(self):
        response = self.client.get(
            REDACTOR_LIST_URL,
            {"username": "redactor1"}
        )
        form = RedactorUsernameSearchForm(data={"username": "redactor1"})
        self.assertTrue(form.is_valid())
        self.assertContains(response, "redactor1")

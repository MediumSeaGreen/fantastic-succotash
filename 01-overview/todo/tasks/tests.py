from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Todo


class TodoViewsTests(TestCase):
    def test_create_todo(self):
        response = self.client.post(
            reverse("tasks:create"),
            {
                "title": "Buy milk",
                "description": "2% milk",
                "due_date": "2030-01-01",
                "is_resolved": False,
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("tasks:list"))
        self.assertEqual(Todo.objects.count(), 1)
        todo = Todo.objects.first()
        self.assertEqual(todo.title, "Buy milk")
        self.assertEqual(todo.due_date, date(2030, 1, 1))

    def test_list_shows_todos(self):
        Todo.objects.create(title="Read a book")
        response = self.client.get(reverse("tasks:list"))
        self.assertContains(response, "Read a book")

    def test_update_todo(self):
        todo = Todo.objects.create(title="Initial")
        response = self.client.post(
            reverse("tasks:edit", args=[todo.pk]),
            {
                "title": "Updated",
                "description": "Details",
                "due_date": "2030-05-01",
                "is_resolved": True,
            },
        )
        self.assertRedirects(response, reverse("tasks:list"))
        todo.refresh_from_db()
        self.assertEqual(todo.title, "Updated")
        self.assertTrue(todo.is_resolved)

    def test_toggle_resolved(self):
        todo = Todo.objects.create(title="Toggle me")
        response = self.client.post(reverse("tasks:toggle", args=[todo.pk]))
        self.assertRedirects(response, reverse("tasks:list"))
        todo.refresh_from_db()
        self.assertTrue(todo.is_resolved)

    def test_delete_todo(self):
        todo = Todo.objects.create(title="Delete me")
        response = self.client.post(reverse("tasks:delete", args=[todo.pk]))
        self.assertRedirects(response, reverse("tasks:list"))
        self.assertEqual(Todo.objects.count(), 0)

# Create your tests here.

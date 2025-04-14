from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class StatusIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.status_data = {'name': 'Test Status'}
        self.status = Status.objects.create(name='Existing Status')

        # Пользователь для тестов (если требуется авторизация)
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_status_index_view(self):
        response = self.client.get(reverse('status_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Existing Status')
        self.assertTemplateUsed(response, 'statuses/index.html')

    def test_status_create_view(self):
        response = self.client.post(
            reverse('status_create'),
            data=self.status_data,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Status.objects.filter(name='Test Status').exists())

        # Проверяем сообщение об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно создан')

    def test_status_update_view(self):
        response = self.client.post(
            reverse('status_update', kwargs={'pk': self.status.pk}),
            data={'name': 'Updated Status'},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

        # Проверяем сообщение об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно изменен')

    def test_status_delete_view(self):
        response = self.client.post(
            reverse('status_delete', kwargs={'pk': self.status.pk}),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

        # Проверяем сообщение об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно удален')

    def test_status_delete_protected(self):
        # Создаем задачу с этим статусом
        Task.objects.create(
            name='Test Task',
            status=self.status,
            author=self.user
        )

        response = self.client.post(
            reverse('status_delete', kwargs={'pk': self.status.pk}),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())

        # Проверяем сообщение об ошибке
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Невозможно удалить статус, потому что он используется'
        )

    def test_status_views_unauthenticated(self):
        self.client.logout()

        urls = [
            reverse('status_index'),
            reverse('status_create'),
            reverse('status_update', kwargs={'pk': 1}),
            reverse('status_delete', kwargs={'pk': 1}),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)

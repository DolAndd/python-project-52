from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from task_manager.labels.models import Label

# Create your tests here.


class LabelIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.label_data = {'name': 'Test Label'}
        self.existing_label = Label.objects.create(name='Existing Label')

        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_label_index_view(self):
        response = self.client.get(reverse('label_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Existing Label')
        self.assertTemplateUsed(response, 'labels/index.html')

    def test_label_create_view(self):
        response = self.client.post(
            reverse('label_create'),
            data=self.label_data,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Label.objects.filter(name='Test Label').exists())

        # Проверяем сообщение об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), _("Label created successfully"))

    def test_label_update_view(self):
        response = self.client.post(
            reverse('label_update', kwargs={'pk': self.existing_label.pk}),
            data={'name': 'Updated Label'},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.existing_label.refresh_from_db()
        self.assertEqual(self.existing_label.name, 'Updated Label')

        # Проверяем сообщение об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), _("Label changed successfully"))

    def test_label_delete_view(self):
        response = self.client.post(
            reverse('label_delete', kwargs={'pk': self.existing_label.pk}),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Label.objects.filter(pk=self.existing_label.pk).exists())

        # Проверяем сообщение об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), _("Label removed successfully"))

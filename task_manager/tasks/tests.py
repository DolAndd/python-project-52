from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

# Create your tests here.


class TaskIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = get_user_model().objects.create_user(
            username='user1',
            password='password123'
        )
        self.user2 = get_user_model().objects.create_user(
            username='user2',
            password='password123'
        )
        self.status = Status.objects.create(name='Status1')
        self.label = Label.objects.create(name='Label1')

        self.task_data = {
            'name': 'Test Task',
            'description': 'Test Description',
            'status': self.status.id,
            'executor': self.user2.id,
            'labels': [self.label.id]
        }

        self.task = Task.objects.create(
            name='Existing Task',
            description='Existing Description',
            status=self.status,
            author=self.user1,
            executor=self.user2
        )
        self.task.labels.add(self.label)

    def test_task_list_view(self):
        # Неавторизованный пользователь
        response = self.client.get(reverse('task_index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/tasks/')

        # Авторизованный пользователь
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('task_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Existing Task')
        self.assertTemplateUsed(response, 'tasks/index.html')

    def test_task_create_view(self):
        self.client.login(username='user1', password='password123')

        # GET запрос
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')

        # POST запрос с валидными данными
        response = self.client.post(reverse('task_create'), data=self.task_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_index'))

        # Проверка создания задачи
        task = Task.objects.get(name='Test Task')
        self.assertEqual(task.author, self.user1)
        self.assertEqual(task.executor, self.user2)
        self.assertEqual(task.status, self.status)
        self.assertTrue(task.labels.filter(id=self.label.id).exists())

        # Проверка сообщения об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Задача успешно создана')

    def test_task_update_view(self):
        self.client.login(username='user1', password='password123')
        url = reverse('task_update', kwargs={'pk': self.task.pk})

        # GET запрос
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')

        # POST запрос с обновленными данными
        updated_data = self.task_data.copy()
        updated_data['name'] = 'Updated Task'
        response = self.client.post(url, data=updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_index'))

        # Проверка обновления задачи
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

        # Проверка сообщения об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Задача успешно изменена')

    def test_task_delete_view(self):
        self.client.login(username='user1', password='password123')
        url = reverse('task_delete', kwargs={'pk': self.task.pk})

        # GET запрос
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/delete.html')

        # POST запрос (удаление)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_index'))

        # Проверка удаления задачи
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task.pk)

        # Проверка сообщения об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Задача успешно удалена')

    def test_task_delete_by_non_author(self):
        # Попытка удаления задачи не автором
        self.client.login(username='user2', password='password123')
        url = reverse('task_delete', kwargs={'pk': self.task.pk})

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_index'))

        # Проверка, что задача не удалена
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

        # Проверка сообщения об ошибке
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Задачу может удалить только ее автор')

    def test_task_detail_view(self):
        self.client.login(username='user1', password='password123')
        url = reverse('task_detail', kwargs={'pk': self.task.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/detail.html')
        self.assertContains(response, self.task.name)
        self.assertContains(response, self.task.description)
        self.assertContains(response, self.task.status.name)
        self.assertContains(response, self.task.author.first_name)
        self.assertContains(response, self.task.author.last_name)
        if self.task.executor:
            self.assertContains(response, self.task.executor.first_name)
            self.assertContains(response, self.task.executor.last_name)
        self.assertContains(response, self.label.name)
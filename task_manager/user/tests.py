from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
import json
# Create your tests here.

User = get_user_model()


class UsersTest(TestCase):
    # указываем имена фикстур для загрузки
    fixtures = ['users.json']

    def setUp(self):
        # Получаем пользователя из фикстуры
        self.existing_user = User.objects.get(username='Abius')


    def test_user_registration(self):
        url = reverse('user_create')
        data = {
            'username': 'new_user',
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        # Редирект после успешной регистрации

        # Проверяем, что пользователь создан
        self.assertTrue(User.objects.filter(username='new_user').exists())

    def test_user_update(self):
        # 1. Создаём пользователя для обновления
        user_to_update = User.objects.create_user(
            username='testuser',
            first_name='Original',
            last_name='User',
            password='testpass123')

        # 2. Авторизуем этого пользователя (так как право на удаление только у владельца)
        self.client.force_login(user_to_update)

        # 3. Отправляем POST-запрос на удаление
        url = reverse('user_update', kwargs={'pk': user_to_update.pk})
        update_data = {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'Name',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(url, update_data)

        # 4. Проверяем ответ
        self.assertRedirects(response, '/users/')  # Редирект после успеха

        # 5. Обновляем объект из базы
        user_to_update.refresh_from_db()

        # 6. Проверяем изменения
        self.assertEqual(user_to_update.username, 'updateduser')
        self.assertEqual(user_to_update.first_name, 'Updated')
        self.assertEqual(user_to_update.last_name, 'Name')

    def test_user_delete(self):
        # 1. Создаем пользователя для удаления
        user_to_delete = User.objects.create_user(
            username='to_delete',
            email='delete@example.com',
            password='testpass123'
        )

        # 2. Авторизуем этого пользователя (так как право на удаление только у владельца)
        self.client.force_login(user_to_delete)

        # 3. Отправляем POST-запрос на удаление
        url = reverse('user_delete', kwargs={'pk': user_to_delete.pk})
        response = self.client.post(url)

        # 4. Проверяем редирект (302) после успешного удаления
        self.assertEqual(response.status_code, 302)

        # 5. Проверяем, что пользователь действительно удален
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=user_to_delete.pk)

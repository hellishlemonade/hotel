from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client

from user.forms import SignUpForm
from hotel.constants import NAME_MAX_LENGTH, EMAIL_MAX_LENGTH


User = get_user_model()


class SignUpFormTest(TestCase):
    """Тесты для формы регистрации"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.valid_data = {
            'email': 'newuser@example.com',
            'first_name': 'Новый',
            'last_name': 'Пользователь',
            'password1': 'SecurePassword123!',
            'password2': 'SecurePassword123!'
        }

    def test_form_debug_validation_errors(self):
        """Тест для отладки ошибок валидации формы"""
        form = SignUpForm(data=self.valid_data)
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
            print(f"Form non_field_errors: {form.non_field_errors()}")
            for field_name, errors in form.errors.items():
                print(f"Field {field_name}: {errors}")
        self.assertTrue(form.is_valid())

    def test_form_valid_data(self):
        """Тест валидных данных формы"""
        form = SignUpForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_email(self):
        """Тест невалидного email"""
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalid-email'
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_password_mismatch(self):
        """Тест несовпадения паролей"""
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'differentpassword'
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_missing_required_fields(self):
        """Тест отсутствия обязательных полей"""
        invalid_data = self.valid_data.copy()
        del invalid_data['email']
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

        invalid_data = self.valid_data.copy()
        del invalid_data['first_name']
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

        invalid_data = self.valid_data.copy()
        del invalid_data['last_name']
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

    def test_form_save_creates_user(self):
        """Тест что форма создает пользователя при сохранении"""
        form = SignUpForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertEqual(user.first_name, self.valid_data['first_name'])
        self.assertEqual(user.last_name, self.valid_data['last_name'])
        self.assertTrue(user.check_password(self.valid_data['password1']))

    def test_form_fields(self):
        """Тест что форма содержит правильные поля"""
        form = SignUpForm()
        expected_fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_form_email_max_length_validation(self):
        """Тест валидации максимальной длины email через форму"""
        long_email = 'a' * (EMAIL_MAX_LENGTH - 10) + '@test.com'
        if len(long_email) > EMAIL_MAX_LENGTH:
            invalid_data = self.valid_data.copy()
            invalid_data['email'] = long_email
            form = SignUpForm(data=invalid_data)
            self.assertFalse(form.is_valid())
            self.assertIn('email', form.errors)

    def test_form_name_max_length_validation(self):
        """Тест валидации максимальной длины имени и фамилии через форму"""
        long_name = 'А' * (NAME_MAX_LENGTH + 1)

        invalid_data = self.valid_data.copy()
        invalid_data['first_name'] = long_name
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

        invalid_data = self.valid_data.copy()
        invalid_data['last_name'] = long_name
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

    def test_form_empty_fields_validation(self):
        """Тест валидации пустых полей"""
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = ''
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

        invalid_data = self.valid_data.copy()
        invalid_data['first_name'] = ''
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

        invalid_data = self.valid_data.copy()
        invalid_data['last_name'] = ''
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

    def test_form_password_validation(self):
        """Тест валидации паролей"""
        invalid_data = self.valid_data.copy()
        invalid_data['password1'] = '123'
        invalid_data['password2'] = '123'
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

        invalid_data = self.valid_data.copy()
        invalid_data['password1'] = '12345678'
        invalid_data['password2'] = '12345678'
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_creates_active_user(self):
        """Тест что форма создает активного пользователя"""
        form = SignUpForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNotNone(user.date_joined)


class UserRegistrationWorkflowTest(TestCase):
    """Тесты полного процесса регистрации пользователя"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.client = Client()
        self.valid_data = {
            'email': 'workflow@example.com',
            'first_name': 'Рабочий',
            'last_name': 'Процесс',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }

    def test_complete_user_registration_workflow(self):
        """Тест полного процесса регистрации пользователя"""

        form = SignUpForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertTrue(
            User.objects.filter(email=self.valid_data['email']).exists())

        self.assertEqual(user.email, self.valid_data['email'])
        self.assertEqual(user.first_name, self.valid_data['first_name'])
        self.assertEqual(user.last_name, self.valid_data['last_name'])
        self.assertTrue(user.check_password(self.valid_data['password1']))

        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.is_active)

    def test_multiple_user_registration(self):
        """Тест регистрации нескольких пользователей"""
        users_data = [
            {
                'email': 'user1@example.com',
                'first_name': 'Пользователь',
                'last_name': 'Первый',
                'password1': 'SecurePass1!',
                'password2': 'SecurePass1!'
            },
            {
                'email': 'user2@example.com',
                'first_name': 'Пользователь',
                'last_name': 'Второй',
                'password1': 'SecurePass2!',
                'password2': 'SecurePass2!'
            }
        ]

        created_users = []
        for user_data in users_data:
            form = SignUpForm(data=user_data)
            self.assertTrue(form.is_valid())
            user = form.save()
            created_users.append(user)

        self.assertEqual(len(created_users), 2)
        self.assertEqual(User.objects.count(), 2)

        emails = [user.email for user in created_users]
        self.assertEqual(len(emails), len(set(emails)))

    def test_user_registration_with_duplicate_email(self):
        """Тест попытки регистрации с существующим email"""
        # Создаем первого пользователя
        form1 = SignUpForm(data=self.valid_data)
        self.assertTrue(form1.is_valid())
        form1.save()

        duplicate_data = self.valid_data.copy()
        duplicate_data['first_name'] = 'Другой'
        duplicate_data['last_name'] = 'Пользователь'

        form2 = SignUpForm(data=duplicate_data)
        self.assertFalse(form2.is_valid())
        self.assertIn('email', form2.errors)

        self.assertEqual(
            User.objects.filter(email=self.valid_data['email']).count(), 1)

    def test_user_registration_data_persistence(self):
        """Тест сохранения всех данных пользователя"""
        form = SignUpForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

        form.save()

        saved_user = User.objects.get(email=self.valid_data['email'])
        self.assertEqual(saved_user.email, self.valid_data['email'])
        self.assertEqual(saved_user.first_name, self.valid_data['first_name'])
        self.assertEqual(saved_user.last_name, self.valid_data['last_name'])
        self.assertTrue(saved_user.check_password(self.valid_data['password1']))

        self.assertIsNotNone(saved_user.date_joined)

        self.assertIsNone(saved_user.last_login)
        self.assertTrue(saved_user.is_active)
        self.assertFalse(saved_user.is_staff)
        self.assertFalse(saved_user.is_superuser)


class ProfileModelPropertiesTest(TestCase):
    """Тесты свойств модели Profile через форму"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.user_data = {
            'email': 'properties@example.com',
            'first_name': 'Свойства',
            'last_name': 'Модели',
            'password1': 'SecurePass456!',
            'password2': 'SecurePass456!'
        }

    def test_user_string_representation(self):
        """Тест строкового представления пользователя"""
        form = SignUpForm(data=self.user_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(str(user), self.user_data['email'])

    def test_user_username_field_is_email(self):
        """Тест что USERNAME_FIELD установлен как email"""
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_user_required_fields(self):
        """Тест обязательных полей"""
        self.assertIn('first_name', User.REQUIRED_FIELDS)
        self.assertIn('last_name', User.REQUIRED_FIELDS)

    def test_user_meta_verbose_names(self):
        """Тест verbose names в Meta классе"""
        form = SignUpForm(data=self.user_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user._meta.verbose_name, 'пользователь')
        self.assertEqual(user._meta.verbose_name_plural, 'Пользователи')

    def test_user_meta_ordering(self):
        """Тест сортировки по умолчанию"""

        user_data1 = {
            'email': 'b@example.com',
            'first_name': 'Борис',
            'last_name': 'Борисов',
            'password1': 'SecurePass789!',
            'password2': 'SecurePass789!'
        }

        user_data2 = {
            'email': 'a@example.com',
            'first_name': 'Алексей',
            'last_name': 'Алексеев',
            'password1': 'SecurePass012!',
            'password2': 'SecurePass012!'
        }

        form1 = SignUpForm(data=user_data1)
        self.assertTrue(form1.is_valid())
        user1 = form1.save()

        form2 = SignUpForm(data=user_data2)
        self.assertTrue(form2.is_valid())
        user2 = form2.save()

        users = User.objects.all()
        self.assertEqual(users[0], user2)
        self.assertEqual(users[1], user1)

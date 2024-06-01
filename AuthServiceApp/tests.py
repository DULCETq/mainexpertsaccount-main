from django.test import TestCase
from django.contrib.auth.models import User
from .models import Account, Client, Expert
from django.contrib.auth import login, authenticate
from .functions import full_registration_client
import datetime
import json


class AuthTestCase(TestCase):
    def setUp(self):
        """Подготовка базы"""
        self.credentials = {
            'username': 'test2@email.ru',
            'password': 'testpass12'
        }
        self.credentials_no_auth = {
            'username': 'test21@email.ru',
            'password': 'testpass121'
        }
        self.user = User.objects.create_user(**self.credentials)
        self.user_noauth = User.objects.create_user(**self.credentials_no_auth)

        Account.objects.create(user=self.user,
                               name='test',
                               user_type='Client',
                               phone='897755331123',
                               age=43,
                               is_active=True,
                               available_balance=0
                               )
        Account.objects.create(user=self.user_noauth,
                               name='user_noauth',
                               user_type='user_noauth',
                               phone='897755331113',
                               age=40,
                               is_active=True,
                               available_balance=0
                               )

    def tearDown(self):
        """Удаление базы"""
        User.objects.all().delete()

    def test_hard_code(self):
        """Проверка в хард коде, что по верным данным пользователь может авторизоваться"""
        user = authenticate(**self.credentials)
        self.assertTrue(user is not None and user.is_authenticated)

    def test_check_auth(self):
        """Успешная проверка авторизации пользователя"""
        self.client.login(**self.credentials)
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.get('/check_auth/')
        self.assertTrue(json.loads(response.data)['auth_status'])

    def test_check_auth_fail(self):
        """Неуспешная проверка авторизации пользователя"""
        response = self.client.get('/check_auth/')
        self.assertFalse(json.loads(response.data)['auth_status'])

    def test_correct(self):
        """Проверка авторизации с верными данными"""
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(json.loads(response.data)['success'])

    def test_wrong_username(self):
        """Проверка авторизации с неверным логином"""
        response = self.client.post('/login/', {'username': 'wrong', 'password': 'testpass12'})
        self.assertFalse(json.loads(response.data)['success'])

    def test_wrong_pssword(self):
        """Проверка авторизации с неверным паролем"""
        response = self.client.post('/login/', {'username': 'test@email.ru', 'password': 'wrong'})
        self.assertFalse(json.loads(response.data)['success'])


class RegisterTestCase(TestCase):
    def setUp(self):
        """Подготовка базы"""
        self.credentials = {
            'username': 'test2@email.ru',
            'password': 'testpass12'
        }
        user = User.objects.create_user(**self.credentials)

        Account.objects.create(user=user,
                               name='test',
                               user_type='Client',
                               phone='+79900012121',
                               age=43,
                               is_active=True,
                               available_balance=0
                               )

    def tearDown(self):
        """Удаление базы"""
        User.objects.all().delete()

    def test_registration_correct(self):
        data = {
            'user_type': 'Client',
            'phone': '+7-(990)-001-21-12',
            'email': 'test1@email.com',
            'name': 'TestCorrect',
            'password': 'pass1234',
            'confirm_password': 'pass1234'
        }
        response = self.client.post('/register/', data)
        self.assertTrue(json.loads(response.data)['success'])

    def test_registration_missing_data(self):
        data = {
            'user_type': 'Client',
            'phone': '+7-(990)-001-21-12',
            'email': 'test1@email.com',
            'name': 'TestCorrect',
        }
        response = self.client.post('/register/', data)
        self.assertFalse(json.loads(response.data)['success'])

    def test_registration_existing_email(self):
        data = {
            'user_type': 'Client',
            'phone': '+7-(990)-001-21-12',
            'email': 'test2@email.ru',
            'name': 'TestCorrect',
            'password': 'pass1234',
            'confirm_password': 'pass1234'
        }
        response = self.client.post('/register/', data)
        self.assertFalse(json.loads(response.data)['success'])

    def test_registration_existing_phone(self):
        data = {
            'user_type': 'Client',
            'phone': '+7-(990)-001-21-21',
            'email': 'test2daw@email.ru',
            'name': 'TestCorrect',
            'password': 'pass1234',
            'confirm_password': 'pass1234'
        }
        response = self.client.post('/register/', data)
        self.assertFalse(json.loads(response.data)['success'])


class FullRegistrationTestCase(TestCase):
    def setUp(self):
        """Подготовка базы"""
        self.credentials = {
            'username': 'test2@email.ru',
            'password': 'testpass12'
        }
        user = User.objects.create_user(**self.credentials)
        self.full_registration_data_correct = {'client_id': user.id,
                                               'place_of_study_name': 'MSU',
                                               'education_date_start': datetime.date(2021, 1, 12),
                                               'education_date_end': datetime.date(2021, 6, 12),
                                               'education_type': 'phd',
                                               'favorite_lessons': None,
                                               'goals': None}
        self.full_registration_data_error = {'place_of_study_name': 'MSU',
                                             'education_date_start': datetime.date(2021, 1, 12),
                                             'education_date_end': datetime.date(2021, 6, 12),
                                             'education_type': 'phd',
                                             'favorite_lessons': None,
                                             'goals': None}
        Account.objects.create(user=user,
                               name='test',
                               user_type='Client',
                               phone='+79900012121',
                               age=43,
                               is_active=True,
                               available_balance=0
                               )

    def tearDown(self):
        """Удаление базы"""
        User.objects.all().delete()

    def test_full_registration_hardcode(self):
        response = full_registration_client(self.full_registration_data_correct)
        self.assertTrue(response)

    def test_full_registration_correct(self):
        response = self.client.post('register/full/client', self.full_registration_data_correct)
        self.assertTrue(json.loads(response.data)['success'])

    def test_full_registration_missing_data(self):
        response = self.client.post('register/full/client', self.full_registration_data_error)
        self.assertFalse(json.loads(response.data)['success'])
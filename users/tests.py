from django.test import TestCase
from .models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test@mail.com"
        cls.first_name = "jonh"
        cls.last_name = "doe"
        cls.password = "1234"
        
        cls.user = User.objects.create(
            email=cls.email,
            first_name=cls.first_name,
            last_name=cls.last_name,
            password=cls.password,
        )
        
    def test_email_unique(self):
        account = User.objects.get(id=self.user.id)
        unique = account._meta.get_field("email").unique
        self.assertEquals(unique, True)
        
    def test_first_name_max_length(self):
        account = User.objects.get(id=self.user.id)
        max_length = account._meta.get_field("first_name").max_length
        self.assertEquals(max_length, 30)

    def test_last_name_max_length(self):
        account = User.objects.get(id=self.user.id)
        max_length = account._meta.get_field("last_name").max_length
        self.assertEquals(max_length, 30)

    def test_password_max_length(self):
        account = User.objects.get(id=self.user.id)
        max_length = account._meta.get_field("password").max_length
        self.assertEquals(max_length, 200)


class UserViewsTest(APITestCase):
    
    def test_create_account_view(self):
        response = self.client.post(
            "/api/users/register/",
            {
                "first_name": "jonh",
                "last_name": "doe",
                "email": "test@mail.com",
                "password": "1234",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        
        
    def test_login_view(self):
        self.client.post(
            "/api/users/register/",
            {
                "first_name": "jonh",
                "last_name": "doe",
                "email": "test@mail.com",
                "password": "1234",
            },
            format="json",
        )

        response = self.client.post(
            "/api/users/login/",
            {
                "email": "test@mail.com",
                "password": "1234",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        
        
class UserViewsTest(APITestCase):
    
    def setUp(self):
      user = User.objects.create(first_name='user', last_name='last_name', password='password', email='test@mail.com')
      token = Token.objects.create(user=user)

      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    def test_path_view(self):        
        response = self.client.patch(
            "/api/users/profile/",
            {
                "email": "patch@mail.com"
            },
            format="json",
        )
        
        self.assertEqual(response.status_code, 200)
        
    def test_delete_view(self):        
        response = self.client.delete(
            "/api/users/profile/"
        )
        
        self.assertEqual(response.status_code, 204)
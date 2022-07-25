from django.test import TestCase
from .models import Anime
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from categories.models import Category
from users.models import User

class AnimeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.image = "image.png"
        cls.title = "One piece"
        cls.sinopse = "Um anime para otakus de verdade."
        cls.studio = "Toei animation"
        cls.banner = "banner.png"
        cls.original_title = "One piece"
        cls.launch_data = "1997-01-02"
        cls.average_rate = 7
        cls.status="on Going"
        cls.new_category= Category.objects.create(category="ação")

        cls.anime_obj =Anime.objects.create(
            image = cls.image,
            title = cls.title,
            sinopse = cls.sinopse,
            studio = cls.studio,
            banner = cls.banner,
            original_title = cls.original_title,
            launch_data = cls.launch_data,
            average_rate = cls.average_rate,
            status = cls.status,
        )
        cls.anime_obj.categories.add(cls.new_category)
        cls.anime_obj.save()
            

    def test_anime_fields(self):
        
        self.assertIsInstance(self.anime_obj.image, str),
        self.assertEqual(self.anime_obj.image, self.image)
        
        self.assertIsInstance(self.anime_obj.title, str),
        self.assertEqual(self.anime_obj.title, self.title)
        
        self.assertIsInstance(self.anime_obj.sinopse, str),
        self.assertEqual(self.anime_obj.sinopse, self.sinopse)
        
        self.assertIsInstance(self.anime_obj.studio, str),
        self.assertEqual(self.anime_obj.studio, self.studio)
        
        self.assertIsInstance(self.anime_obj.banner, str),
        self.assertEqual(self.anime_obj.banner, self.banner)
        
        self.assertIsInstance(self.anime_obj.original_title, str),
        self.assertEqual(self.anime_obj.original_title, self.original_title)
        
        self.assertIsInstance(self.anime_obj.launch_data, str),
        self.assertEqual(self.anime_obj.launch_data, self.launch_data)
        
        self.assertIsInstance(self.anime_obj.average_rate, int),
        self.assertEqual(self.anime_obj.average_rate, self.average_rate)
        
        self.assertIsInstance(self.anime_obj.status, str),
        self.assertEqual(self.anime_obj.status, self.status)
        
        self.assertIsInstance(self.anime_obj.categories.first(), Category)
        self.assertEqual(self.anime_obj.categories.first(), self.new_category)

class AnimeViewsAdminTest(APITestCase):
    def setUp(self):
      user = User.objects.create_superuser(email="admin@kenzie.com", first_name='user', last_name="name", password='password',)
      token = Token.objects.create(user=user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_anime_view(self):
        response = self.client.post(
            "/api/animes/",
            {
                "image": "logeo.png",
                "title":"The witceher",
                "sinopse":"blableabla",
                "studio":"marqeuinho produções",
                "banner":"bannere.png",
                "original_title":"the witcher",
                "launch_data": "2022-07-15",
                "status": "On going",
                "categories": [{"category": "açeão" } , {"category": "batata"}]
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
    
    def test_create_anime_view_missing_image(self):
        response = self.client.post(
            "/api/animes/",
            {
                
                "title":"The witceher",
                "sinopse":"blableabla",
                "studio":"marqeuinho produções",
                "banner":"bannere.png",
                "original_title":"the witcher",
                "launch_data": "2022-07-15",
                "status": "On going",
                "categories": [{"category": "açeão" } , {"category": "batata"}]
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
    
    def test_create_anime_view_missing_categories(self):
        response = self.client.post(
            "/api/animes/",
            {
                "image": "logeo.png",
                "title":"The witceher",
                "sinopse":"blableabla",
                "studio":"marqeuinho produções",
                "banner":"bannere.png",
                "original_title":"the witcher",
                "launch_data": "2022-07-15",
                "status": "On going"
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        
    def get_all_animes_view(self):
        response = self.client.get("/api/animes/")

        self.assertEqual(response.status_code, 201)

class AnimeViewsNormalUserTest(APITestCase):
    def setUp(self):
      user = User.objects.create(email="user@email.com", first_name='user', last_name="name", password='password',)
      token = Token.objects.create(user=user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_anime_view(self):
        response = self.client.post(
            "/api/animes/",
            {
                "image": "logeo.png",
                "title":"The witceher",
                "sinopse":"blableabla",
                "studio":"marqeuinho produções",
                "banner":"bannere.png",
                "original_title":"the witcher",
                "launch_data": "2022-07-15",
                "status": "On going",
                "categories": [{"category": "açeão" } , {"category": "batata"}]
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def get_all_animes_view(self):
        response = self.client.get("/api/animes/")

        self.assertEqual(response.status_code, 201)

class AnimeViewsWithoutTokenTest(APITestCase):

    def test_create_anime_view(self):
        response = self.client.post(
            "/api/animes/",
            {
                "image": "logeo.png",
                "title":"The witceher",
                "sinopse":"blableabla",
                "studio":"marqeuinho produções",
                "banner":"bannere.png",
                "original_title":"the witcher",
                "launch_data": "2022-07-15",
                "status": "On going",
                "categories": [{"category": "açeão" } , {"category": "batata"}]
            },
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def get_all_animes_view(self):
        response = self.client.get("/api/animes/")

        self.assertEqual(response.status_code, 401)

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from users.models import User

class UserslistViewsText(APITestCase):
    def setUp(self):
        user = User.objects.create(
            first_name="user",
            last_name="last_name",
            password="password",
            email="test@mail.com",
            is_superuser=True,
        )
        token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        
    def test_post_view(self):
        anime = self.client.post(
            "/api/animes/",
            {
                "image": "logeo.png",
                "title": "The witceher",
                "sinopse": "blableabla",
                "studio": "marqeuinho produções",
                "banner": "bannere.png",
                "original_title": "the witcher",
                "launch_data": "2022-07-15",
                "status": "Finished",
                "categories": [{"category": "açeão"}, {"category": "batata"}],
                "average_rate": 0,
            },
            format="json",
        )
        
        response = self.client.post(
            f'/api/userlist/{anime.data["id"]}/',
            {"watching_status": "Terminado"},
            format="json",
        )
        self.assertEqual(response.status_code,201)

    def test_list_all_view(self):
        response = self.client.get("/api/userlist/")
        self.assertEqual(response.status_code, 200)


    def test_update_view(self):
        anime = self.client.post(
            "/api/animes/",
            {
                "image": "logeo.png",
                "title": "The witceher",
                "sinopse": "blableabla",
                "studio": "marqeuinho produções",
                "banner": "bannere.png",
                "original_title": "the witcher",
                "launch_data": "2022-07-15",
                "status": "Finished",
                "categories": [{"category": "açeão"}, {"category": "batata"}],
                "average_rate": 0,
            },
            format="json",
        )

        my_anime = self.client.post(
            f'/api/userlist/{anime.data["id"]}/',
            {"watching_status": "Terminado"},
            format="json",
        )

        response = self.client.patch(
            f'/api/userlist/myanimes/{my_anime.data["id"]}/',
            {"watching_status": "Terminado"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
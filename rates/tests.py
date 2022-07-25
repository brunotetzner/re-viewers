from users.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RateViewsTest(APITestCase):
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
            "/api/rate/",
            {"anime_id": anime.data["id"], "rate": 4},
            format="json",
        )

        self.assertEqual(response.status_code, 201)

    def test_path_view(self):
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

        self.client.post(
            "/api/rate/",
            {"anime_id": anime.data["id"], "rate": 4},
            format="json",
        )

        response = self.client.patch(
            f'/api/rate/{anime.data["id"]}/',
            {"rate": 1},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

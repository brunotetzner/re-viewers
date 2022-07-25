from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.models import Userlist

class UserslistViewsText(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.anime = {
            "id": "sauhsaushaushua",
            "image":"jojo.png",
            "title":"jojo",
            "sinopse":"jojo",
            "studio":"jojo",
            "banner":"jojojo.png",
            "original_title":"jojo",
            "launch_data":"jojo",
            "average_rate":"jojo",
            "status":"On Going",
        }

        cls.user = {
            "email":"bernardo@mail.com",
            "first_name":"bernardo",
            "last_name":"costa",
            "password":"loona",
        }

        cls.anime_to_list = {
            "watching_status": "Terminado"
        }

    def test_user_adding_anime_to_userlist(self):

        self.client.post(
            "api/users/register/", 
            self.user, 
            format="json"
            )

        login_data = {
            "email": self.user["email"],
            "password": self.user["password"],
        }
        
        auth = self.client.post(
            "/api/users/login/", 
            login_data, 
            format="json"
            )

        token = auth.data['token']
        # token = auth["token"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token " + token
        )

        anime = self.anime
        anime_id = anime["id"]

        response = self.client.post(
            f"/api/userlist/{anime_id}/",
            # f"/api/userlist/sauhsaushaushua/",
            self.anime_to_list,
            format="json"
            )
        
        self.assertEquals(response.status_code, 201)

    def test_userlist_getting(self):

        self.client.post(
            "api/users/register/", 
            self.user, 
            format="json"
            )

        login_data = {
            "email": self.user["email"],
            "password": self.user["password"],
        }
        
        auth = self.client.post(
            "/api/users/login/", 
            login_data, 
            format="json"
            )

        token = auth.data['token']
        # token = auth["token"]

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token
        )

        response = self.client.get("/api/userlist/")
        
        self.assertEqual(response.status_code, 200)

from django.test import TestCase
from animes.models import Anime

from users.models import User, Userlist

class UserlistModelTest(TestCase):
    @classmethod

    def setUpTestData(cls):
        cls.email = "bernardo@mail.com"
        cls.first_name = "bernardo"
        cls.last_name = "costa"
        cls.password = "1234"
        
        cls.user = User.objects.create(
            email=cls.email,
            first_name=cls.first_name,
            last_name=cls.last_name,
            password=cls.password,
        )

        cls.image = "jojo.png"
        cls.title = "Jojo"
        cls.sinopse = "Tudo começa quando o Jonathan perde a cabeça..."
        cls.studio = "Davi produções"
        cls.banner = "jojojo.png"
        cls.original_title = "JJBA"
        cls.launch_data = "2022-07-22"
        cls.average_rate = 5
        cls.status = "On going"

        cls.anime = Anime.objects.create(
            image=cls.image,
            title=cls.title,
            sinopse=cls.sinopse,
            studio=cls.studio,
            banner=cls.banner,
            original_title=cls.original_title,
            launch_data=cls.launch_data,
            average_rate=cls.average_rate,
            status=cls.status,
        )

        cls.watching_status = "Terminado"

        cls.userlist = Userlist.objects.create(
            anime=cls.anime,
            user=cls.user,
            watching_status=cls.watching_status
        )

    def test_animelist_has_information_fields(self):
        
        self.assertEqual(self.userlist.anime, self.anime)
        self.assertEqual(self.userlist.user, self.user)
        self.assertEqual(self.userlist.watching_status, self.watching_status)
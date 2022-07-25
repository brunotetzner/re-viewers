# Generated by Django 4.0.6 on 2022-07-22 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("animes", "0005_alter_anime_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="anime",
            name="status",
            field=models.CharField(
                choices=[
                    ("PR", "In Production"),
                    ("CA", "Canceled"),
                    ("FI", "Finished"),
                ],
                max_length=30,
            ),
        ),
    ]

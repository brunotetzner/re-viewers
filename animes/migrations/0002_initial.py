# Generated by Django 4.0.6 on 2022-07-27 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('animes', '0001_initial'),
        ('categories', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='anime',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animes.anime'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='anime',
            name='categories',
            field=models.ManyToManyField(to='categories.category'),
        ),
        migrations.AddField(
            model_name='anime',
            name='comments',
            field=models.ManyToManyField(related_name='Anime_comments', through='animes.Comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='anime',
            name='users',
            field=models.ManyToManyField(through='animes.Rate', to=settings.AUTH_USER_MODEL),
        ),
    ]

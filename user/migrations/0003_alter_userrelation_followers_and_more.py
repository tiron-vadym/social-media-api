# Generated by Django 5.0.3 on 2024-03-20 21:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_user_bio_user_picture_post_userrelation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userrelation",
            name="followers",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="follower_relations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="userrelation",
            name="following",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="following_relations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

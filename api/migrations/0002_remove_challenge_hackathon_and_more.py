# Generated by Django 5.1.4 on 2024-12-10 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="challenge",
            name="hackathon",
        ),
        migrations.RemoveField(
            model_name="hackathon",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="team",
            name="hackathon",
        ),
    ]

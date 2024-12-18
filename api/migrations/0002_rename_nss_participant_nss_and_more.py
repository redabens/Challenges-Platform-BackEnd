# Generated by Django 5.1.4 on 2024-12-14 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participant',
            old_name='Nss',
            new_name='nss',
        ),
        migrations.RenameField(
            model_name='participant',
            old_name='University',
            new_name='university',
        ),
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.EmailField(max_length=200, unique=True),
        ),
    ]

# Generated by Django 3.2.11 on 2022-04-08 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='poster_url',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]

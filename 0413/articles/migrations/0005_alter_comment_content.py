# Generated by Django 3.2.12 on 2022-04-13 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_rename_commnet_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=20),
        ),
    ]

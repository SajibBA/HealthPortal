# Generated by Django 3.0 on 2020-12-28 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20201228_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievements',
            name='achievement_pic',
            field=models.ImageField(blank=True, null=True, upload_to='pics/'),
        ),
    ]

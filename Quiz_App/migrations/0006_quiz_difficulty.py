# Generated by Django 3.1.4 on 2021-02-07 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz_App', '0005_auto_20210207_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='difficulty',
            field=models.CharField(default='easy', max_length=30),
        ),
    ]
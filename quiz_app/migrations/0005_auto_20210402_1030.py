# Generated by Django 3.1.4 on 2021-04-02 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0004_quiz_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(default='Quiz', max_length=50),
        ),
    ]

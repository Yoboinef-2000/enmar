# Generated by Django 5.0.6 on 2024-07-02 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learningPlatform', '0005_lesson_description_userlessoncompletion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpeg', upload_to='profile_pics'),
        ),
    ]
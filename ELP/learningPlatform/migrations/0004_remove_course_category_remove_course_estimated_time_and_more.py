# Generated by Django 5.0.6 on 2024-06-27 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learningPlatform', '0003_course_category_course_estimated_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='category',
        ),
        migrations.RemoveField(
            model_name='course',
            name='estimated_time',
        ),
        migrations.RemoveField(
            model_name='course',
            name='target_audience',
        ),
        migrations.RemoveField(
            model_name='course',
            name='thumbnail',
        ),
    ]

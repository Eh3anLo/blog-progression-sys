# Generated by Django 5.0.6 on 2024-06-07 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='major',
            field=models.CharField(blank=True, choices=[('CS1', 'Computer Associate degree'), ('CS2', "Computer Bachelor's degree"), ('N1', 'Network Associate degree')], max_length=200),
        ),
    ]
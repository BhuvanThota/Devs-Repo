# Generated by Django 5.0.6 on 2024-10-14 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_project_owner'),
        ('users', '0006_alter_profile_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='star',
            field=models.ManyToManyField(blank=True, null=True, related_name='stars', to='users.profile'),
        ),
    ]

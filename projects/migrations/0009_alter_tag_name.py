# Generated by Django 5.0.6 on 2024-10-17 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_project_star_profiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

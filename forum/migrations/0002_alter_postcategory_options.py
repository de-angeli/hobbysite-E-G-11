# Generated by Django 5.1.6 on 2025-03-01 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcategory',
            options={'ordering': ['name'], 'verbose_name': 'Post Category', 'verbose_name_plural': 'Post Categories'},
        ),
    ]

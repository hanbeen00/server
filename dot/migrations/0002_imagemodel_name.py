# Generated by Django 5.0.4 on 2024-05-21 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemodel',
            name='name',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]

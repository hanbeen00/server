# Generated by Django 5.0.4 on 2024-05-08 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dot', '0009_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='address',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]

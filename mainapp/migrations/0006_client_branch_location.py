# Generated by Django 4.2.7 on 2023-12-28 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_client_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='branch_location',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-28 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_client_branch_location'),
        ('testapp', '0004_createuser_is_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createuser',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.client'),
        ),
    ]

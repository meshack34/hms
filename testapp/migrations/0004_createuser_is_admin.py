# Generated by Django 4.2.7 on 2023-12-28 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0003_branchrestrict'),
    ]

    operations = [
        migrations.AddField(
            model_name='createuser',
            name='is_admin',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]

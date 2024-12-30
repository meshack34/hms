# Generated by Django 4.2.5 on 2023-11-28 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BranchRestrict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_limit', models.CharField(max_length=100)),
                ('user_limit', models.CharField(max_length=100)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('branch_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.client')),
            ],
        ),
    ]
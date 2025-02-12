# Generated by Django 4.2.5 on 2023-11-29 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testapp', '0001_initial'),
        ('usermanagementapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='createuser',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='create_user_profile', to='usermanagementapp.screenaccess'),
        ),
        migrations.AddField(
            model_name='corporatemaster',
            name='City',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.citymaster'),
        ),
        migrations.AddField(
            model_name='corporatemaster',
            name='designation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.designation'),
        ),
        migrations.AddField(
            model_name='citymaster',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.districtmaster'),
        ),
        migrations.AddField(
            model_name='centralisedadminview',
            name='Doc_Name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.doctortable'),
        ),
        migrations.AddField(
            model_name='centralisedadminview',
            name='room_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.roomnumber'),
        ),
        migrations.AddField(
            model_name='cancelbillremark',
            name='bill_no',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='testapp.opdbillingmain'),
        ),
        migrations.AddField(
            model_name='cancelbillremark',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cancelbillremark',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='testapp.locationmaster'),
        ),
        migrations.AddField(
            model_name='branchmaster',
            name='group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.groupmaster'),
        ),
        migrations.AddField(
            model_name='bookedappointments',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookedappointments',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='testapp.locationmaster'),
        ),
        migrations.AddField(
            model_name='billinggrouptarifflink',
            name='Billing_Group_Name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.billinggroup'),
        ),
        migrations.AddField(
            model_name='billinggrouptarifflink',
            name='Tariff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.tariffmaster'),
        ),
        migrations.AddField(
            model_name='billinggroupcorporatemaster',
            name='Biiling_Group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.billinggroup'),
        ),
        migrations.AddField(
            model_name='billinggroupcorporatemaster',
            name='Corporate_Name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.corporatemaster'),
        ),
        migrations.AddField(
            model_name='authorizedperson',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.clinicalordepartment'),
        ),
        migrations.AddField(
            model_name='appointmenttable',
            name='doctor_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.doctortable'),
        ),
        migrations.AddField(
            model_name='advpatientvisitmains',
            name='clinical_department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.clinicalordepartment'),
        ),
        migrations.AddField(
            model_name='advpatientvisitmains',
            name='nurse_doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.doctortable'),
        ),
        migrations.AddField(
            model_name='advpatientvisitmains',
            name='visit_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.visittyoemaster'),
        ),
    ]

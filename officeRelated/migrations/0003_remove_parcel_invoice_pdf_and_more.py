# Generated by Django 5.1.2 on 2025-03-09 00:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officeRelated', '0002_alter_branch_branch_incharge_phone_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parcel',
            name='invoice_pdf',
        ),
        migrations.AlterField(
            model_name='parcel',
            name='receiving_branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='receiving_branch', to='officeRelated.branch'),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='sending_branch',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sending_branch', to='officeRelated.branch'),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='tracking_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]

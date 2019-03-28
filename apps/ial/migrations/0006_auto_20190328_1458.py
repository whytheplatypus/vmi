# Generated by Django 2.1.5 on 2019-03-28 14:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ial', '0005_identityassuranceleveldocumentation_verification_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='identityassuranceleveldocumentation',
            name='id',
        ),
        migrations.AddField(
            model_name='identityassuranceleveldocumentation',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]

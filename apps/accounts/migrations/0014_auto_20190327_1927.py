# Generated by Django 2.1.7 on 2019-03-27 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20190320_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.CharField(blank=True, choices=[('female', 'Female'), ('male', 'Male'), ('', 'Unspecified')], default='', help_text='Specify sex, not gender identity.', max_length=6),
        ),
    ]

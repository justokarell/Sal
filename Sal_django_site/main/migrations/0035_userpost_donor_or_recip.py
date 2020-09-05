# Generated by Django 3.0.5 on 2020-08-24 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_auto_20200824_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='donor_or_recip',
            field=models.CharField(choices=[('Donor', 'DONOR'), ('Recipient', 'RECIPIENT'), ('Both', 'BOTH')], default='Donor', max_length=10),
        ),
    ]
# Generated by Django 3.0.5 on 2020-07-14 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20200714_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='org_role',
            field=models.CharField(choices=[('Donor', 'DONOR'), ('Recipient', 'RECIPIENT'), ('Both', 'BOTH')], default='Donor', max_length=10),
        ),
    ]
# Generated by Django 3.2.4 on 2021-10-17 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_personal_economy', '0003_alter_cuenta_nombre'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cuenta',
            unique_together=set(),
        ),
    ]

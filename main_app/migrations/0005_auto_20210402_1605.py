# Generated by Django 2.2.4 on 2021-04-02 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20210402_1602'),
    ]

    operations = [
        migrations.RenameField(
            model_name='password',
            old_name='key',
            new_name='password',
        ),
    ]

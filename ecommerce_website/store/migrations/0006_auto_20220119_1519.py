# Generated by Django 2.2.14 on 2022-01-19 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20220119_1509'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userform',
            old_name='confirmPassword',
            new_name='password1',
        ),
        migrations.RenameField(
            model_name='userform',
            old_name='password',
            new_name='password2',
        ),
    ]
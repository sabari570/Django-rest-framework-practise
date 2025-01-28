# Generated by Django 5.1.1 on 2025-01-28 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_is_active_alter_customuser_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=True, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
    ]

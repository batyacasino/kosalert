# Generated by Django 3.0.6 on 2020-07-15 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kosapp', '0005_reminder_date_completion'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='case_number',
            field=models.CharField(default=123, max_length=50),
            preserve_default=False,
        ),
    ]
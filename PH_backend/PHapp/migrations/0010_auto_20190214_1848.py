# Generated by Django 2.0.2 on 2019-02-14 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PHapp', '0009_auto_20190214_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individuals',
            name='aussie',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='submittedguesses',
            name='correct',
            field=models.BooleanField(default=False),
        ),
    ]

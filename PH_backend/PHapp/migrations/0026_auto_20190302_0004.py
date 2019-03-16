# Generated by Django 2.0.2 on 2019-03-01 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PHapp', '0025_auto_20190224_2254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teams',
            name='avSolve',
        ),
        migrations.AddField(
            model_name='submittedguesses',
            name='pointsAwarded',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='teams',
            name='avHr',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='teams',
            name='avMin',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='teams',
            name='avSec',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='teams',
            name='teamPuzzles',
            field=models.IntegerField(default=0),
        ),
    ]
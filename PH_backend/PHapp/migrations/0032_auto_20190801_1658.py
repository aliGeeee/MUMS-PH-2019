# Generated by Django 2.0.2 on 2019-08-03 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PHapp', '0031_auto_20190628_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='puzzles',
            name='cubelet1',
        ),
        migrations.AddField(
            model_name='puzzles',
            name='guessCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='puzzles',
            name='hyperlinkText',
            field=models.CharField(editable=False, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='puzzles',
            name='metaPart1',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='puzzles',
            name='pdfURI',
            field=models.CharField(editable=False, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='puzzles',
            name='solveCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='puzzles',
            name='solveURI',
            field=models.CharField(editable=False, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='altanswers',
            name='puzzle',
            field=models.ForeignKey(db_column='puzzle', null=True, on_delete=django.db.models.deletion.CASCADE, to='PHapp.Puzzles'),
        ),
        migrations.AlterField(
            model_name='individuals',
            name='team',
            field=models.ForeignKey(db_column='team', null=True, on_delete=django.db.models.deletion.PROTECT, to='PHapp.Teams'),
        ),
        migrations.AlterField(
            model_name='puzzles',
            name='answer',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='puzzles',
            name='hint1',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='puzzles',
            name='hint2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='puzzles',
            name='hint3',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='puzzles',
            name='losePun',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='puzzles',
            name='pdfPath',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='puzzles',
            name='title',
            field=models.CharField(default='Placeholder title', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='puzzles',
            name='winPun',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='submittedguesses',
            name='submitTime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='submittedguesses',
            name='team',
            field=models.ForeignKey(db_column='team', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='teams',
            name='authClone',
            field=models.OneToOneField(db_column='authClone', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]

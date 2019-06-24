# Generated by Django 2.0.2 on 2019-06-23 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PHapp', '0029_auto_20190623_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puzzles',
            name='cubelet1',
            field=models.ForeignKey(db_column='cubelet1', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cubelet1', to='PHapp.Cubelets'),
        ),
        migrations.AlterField(
            model_name='puzzles',
            name='cubelet2',
            field=models.ForeignKey(db_column='cubelet2', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cubelet2', to='PHapp.Cubelets'),
        ),
        migrations.AlterField(
            model_name='puzzles',
            name='cubelet3',
            field=models.ForeignKey(db_column='cubelet3', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cubelet3', to='PHapp.Cubelets'),
        ),
        migrations.AlterField(
            model_name='puzzles',
            name='cubelet4',
            field=models.ForeignKey(db_column='cubelet4', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cubelet4', to='PHapp.Cubelets'),
        ),
        migrations.AlterField(
            model_name='puzzles',
            name='cubelet5',
            field=models.ForeignKey(db_column='cubelet5', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cubelet5', to='PHapp.Cubelets'),
        ),
    ]
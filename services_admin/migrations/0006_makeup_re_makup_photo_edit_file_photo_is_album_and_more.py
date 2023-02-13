# Generated by Django 4.1.5 on 2023-02-10 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services_admin', '0005_alter_makeup_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='makeup',
            name='re_makup',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='photo',
            name='edit_file',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='is_album',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='photo',
            name='number_gate_photo',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='number_location',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='origin_file',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='small_photo',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ranking',
            name='type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='ComboItem',
        ),
    ]

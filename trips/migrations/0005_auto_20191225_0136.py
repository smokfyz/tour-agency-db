# Generated by Django 3.0 on 2019-12-24 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0004_auto_20191225_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visa',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Country', verbose_name='Страна'),
        ),
    ]
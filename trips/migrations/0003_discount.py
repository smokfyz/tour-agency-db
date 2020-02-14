# Generated by Django 3.0 on 2019-12-24 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_auto_20191222_2335'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bought', models.PositiveIntegerField(verbose_name='Количество купленных путевок')),
                ('discount', models.PositiveIntegerField(verbose_name='Размер скидки(%)')),
            ],
        ),
    ]
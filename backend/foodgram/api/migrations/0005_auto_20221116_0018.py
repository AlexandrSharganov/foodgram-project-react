# Generated by Django 2.2.16 on 2022-11-15 20:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20221115_2344'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterField(
            model_name='ingredientamount',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(32767), django.core.validators.MinValueValidator(1)], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(32767), django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления'),
        ),
    ]

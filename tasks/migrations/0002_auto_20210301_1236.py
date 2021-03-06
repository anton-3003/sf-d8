# Generated by Django 2.2.10 on 2021-03-01 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='todoitem',
            options={},
        ),
        migrations.AddField(
            model_name='category',
            name='todos_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

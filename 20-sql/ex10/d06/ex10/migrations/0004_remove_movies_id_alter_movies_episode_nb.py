# Generated by Django 5.0.4 on 2024-11-05 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ex10', '0003_alter_people_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='id',
        ),
        migrations.AlterField(
            model_name='movies',
            name='episode_nb',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]

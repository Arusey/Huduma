# Generated by Django 3.0.3 on 2020-10-23 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0006_auto_20201023_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

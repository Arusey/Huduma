# Generated by Django 3.0.3 on 2020-03-03 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('departments', '0004_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_rating', models.FloatField(default=0)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated_department', to='departments.Department')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rater', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

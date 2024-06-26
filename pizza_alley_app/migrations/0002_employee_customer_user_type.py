# Generated by Django 5.0.6 on 2024-05-13 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_alley_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('firstname', models.CharField(max_length=25)),
                ('lastname', models.CharField(max_length=25)),
                ('user_type', models.IntegerField()),
                ('password', models.CharField(max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='user_type',
            field=models.IntegerField(default=2),
        ),
    ]

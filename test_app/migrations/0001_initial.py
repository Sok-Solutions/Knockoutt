# Generated by Django 4.1.1 on 2022-09-21 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='fragen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('c1', models.CharField(max_length=255)),
                ('c2', models.CharField(max_length=255)),
                ('c3', models.CharField(max_length=255)),
                ('c4', models.CharField(max_length=255)),
            ],
        ),
    ]

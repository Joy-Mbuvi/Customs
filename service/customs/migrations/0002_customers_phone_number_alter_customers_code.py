# Generated by Django 5.1.3 on 2024-11-25 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='phone_number',
            field=models.CharField(default='0000000000', max_length=10),
        ),
        migrations.AlterField(
            model_name='customers',
            name='code',
            field=models.IntegerField(),
        ),
    ]

# Generated by Django 5.1.3 on 2024-12-02 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customs', '0005_alter_customers_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='code',
            field=models.IntegerField(default=33227),
        ),
    ]
# Generated by Django 2.2.1 on 2019-05-13 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190513_0358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='membership',
            field=models.CharField(default='normal', max_length=50),
        ),
        migrations.DeleteModel(
            name='Memberships',
        ),
    ]

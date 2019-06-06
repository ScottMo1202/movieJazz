# Generated by Django 2.1.9 on 2019-06-06 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(choices=[('Movie', 'Movie'), ('Theater', 'Theater'), ('Offer', 'Offer'), ('Authentification', 'Authentification'), ('Transaction', 'Transaction'), ('Others', 'Others')], max_length=100)),
                ('body', models.CharField(max_length=1000)),
                ('answer', models.CharField(max_length=3000, null=True)),
            ],
        ),
    ]

# Generated by Django 2.2.1 on 2019-05-13 01:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Memberships',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=5000)),
                ('runtime', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(500)])),
            ],
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=150, unique=True)),
                ('offer_perc', models.DecimalField(decimal_places=2, max_digits=2)),
                ('description', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Theaters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('street_number', models.CharField(max_length=10)),
                ('street_name', models.CharField(max_length=1000)),
                ('city', models.CharField(max_length=500)),
                ('state', models.CharField(max_length=2)),
                ('post_code', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('movie_type', models.CharField(choices=[('RE', 'Regular'), ('IM', 'IMAX'), ('3D', '3D'), ('RP', 'RPX'), ('4D', '4D')], default='RE', max_length=2)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Movies')),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Theaters')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('membership', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Memberships')),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(200)])),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('offer', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Offers')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Tickets')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Users')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=1000)),
                ('rating', models.CharField(choices=[('1', 'Terrible'), ('2', 'Bad'), ('3', 'Average'), ('4', 'Good'), ('5', 'Excellent')], max_length=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Movies')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Users')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=5000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Movies')),
            ],
        ),
    ]

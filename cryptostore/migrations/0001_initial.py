# Generated by Django 4.0.3 on 2022-03-24 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('coinCode', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('coinRate', models.FloatField(null=True)),
                ('coinCap', models.IntegerField(null=True)),
                ('coinVolume', models.IntegerField(null=True)),
                ('coinIcon', models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CoinHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('coinRate', models.FloatField()),
                ('coinCap', models.IntegerField()),
                ('coinVolume', models.IntegerField()),
                ('coinCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cryptostore.coin')),
            ],
        ),
    ]

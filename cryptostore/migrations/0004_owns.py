# Generated by Django 4.0.3 on 2022-04-03 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cryptostore', '0003_remove_coinhistory_coincode_delete_client_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=10, default=0, max_digits=20)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cryptostore.coin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

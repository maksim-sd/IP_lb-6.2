# Generated by Django 5.1.7 on 2025-05-31 11:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_cinema', '0002_rename_datatime_seance_date_and_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeanceStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Статус сеанса',
                'verbose_name_plural': 'Статусы саенса',
            },
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_cinema.ticketstatus', verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='seance',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api_cinema.seancestatus', verbose_name='Статус'),
        ),
    ]

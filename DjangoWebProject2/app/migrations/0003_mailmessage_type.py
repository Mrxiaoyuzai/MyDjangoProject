# Generated by Django 2.0.5 on 2018-05-14 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180514_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailmessage',
            name='type',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='类别'),
        ),
    ]

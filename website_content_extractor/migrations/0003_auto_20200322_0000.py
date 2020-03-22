# Generated by Django 3.0.4 on 2020-03-22 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_content_extractor', '0002_auto_20200321_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queuetask',
            name='state',
            field=models.CharField(choices=[('pending', 'PENDING'), ('failure', 'FAILURE'), ('success', 'SUCCESS')], default='pending', max_length=20, verbose_name='state'),
        ),
    ]
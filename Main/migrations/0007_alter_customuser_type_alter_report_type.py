# Generated by Django 5.1.7 on 2025-03-28 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0006_alter_customuser_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='type',
            field=models.CharField(choices=[('traffic', 'Traffic'), ('help', 'Help'), ('ambulance', 'Ambulance'), ('fire', 'Fire')], max_length=50),
        ),
        migrations.AlterField(
            model_name='report',
            name='type',
            field=models.CharField(choices=[('traffic', 'Traffic'), ('help', 'Help'), ('ambulance', 'Ambulance'), ('fire', 'Fire')], max_length=20, verbose_name='نوع البلاغ'),
        ),
    ]

# Generated by Django 5.1.7 on 2025-04-08 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0010_alter_ads_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ads',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='ads',
            name='type_ads',
            field=models.IntegerField(blank=True, choices=[(0, 'دارة التطبيق'), (1, 'مرور'), (2, 'الإسعاف'), (3, 'النجدة'), (4, 'المطافئ')], null=True, verbose_name='نوع الإعلان'),
        ),
    ]

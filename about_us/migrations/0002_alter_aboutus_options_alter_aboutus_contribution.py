# Generated by Django 4.2.7 on 2024-08-15 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about_us', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aboutus',
            options={'verbose_name_plural': 'About Us'},
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='contribution',
            field=models.CharField(choices=[('Frontend', 'Frontend'), ('Backend', 'Backend'), ('UI Design', 'UI Design'), ('Full Stack', 'Full Stack')], default='UI Design', max_length=10),
        ),
    ]

# Generated by Django 2.1.2 on 2018-10-19 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Jedi', '0004_padawan_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='padawan',
            name='test',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Jedi.Test'),
        ),
    ]

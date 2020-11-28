# Generated by Django 2.2.7 on 2020-11-28 10:55

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diseases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=100)),
                ('symptom', djongo.models.fields.JSONField()),
                ('answer', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'diseases',
            },
        ),
    ]

# Generated by Django 3.1 on 2021-07-18 04:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwork',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='filmworkperson',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='genrefilmwork',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='person',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id'),
        ),
    ]
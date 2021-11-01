# Generated by Django 3.2.7 on 2021-11-01 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_additionalimage_bb'),
    ]

    operations = [
        migrations.AddField(
            model_name='advuser',
            name='is_activated',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Прошел активацию?'),
        ),
        migrations.AlterField(
            model_name='additionalimage',
            name='bb',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.bb', verbose_name='Объявление'),
        ),
        migrations.AlterField(
            model_name='advuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='bb',
            name='content',
            field=models.TextField(verbose_name='Описание'),
        ),
    ]

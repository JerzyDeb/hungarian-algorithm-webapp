# Generated by Django 3.2.7 on 2022-02-06 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='worker name')),
                ('surname', models.CharField(max_length=64, verbose_name='worker surname')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team', verbose_name='worker team')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='task name')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team', verbose_name='task team')),
            ],
        ),
        migrations.CreateModel(
            name='Execution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='price/time of execution')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.task', verbose_name='task which is executing')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.worker', verbose_name='worker which executes task')),
            ],
        ),
    ]

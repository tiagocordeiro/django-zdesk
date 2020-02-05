# Generated by Django 3.0.2 on 2020-02-04 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado em')),
                ('active', models.BooleanField(default=True, verbose_name='ativo')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('slug', models.SlugField(help_text='This slug is used when building ticket IDs.Once set, try not to change it or e-mailing may get messy.', unique=True, verbose_name='Slug')),
                ('image', models.ImageField(blank=True, null=True, upload_to='queue/')),
            ],
            options={
                'verbose_name': 'Queue',
                'verbose_name_plural': 'Queues',
                'ordering': ('title',),
            },
        ),
    ]
# Generated by Django 2.2 on 2019-04-20 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=400)),
                ('category', models.CharField(choices=[('abstract', 'Abstract'), ('cars', 'Cars'), ('appliances', 'Appliances'), ('gadgets', 'Gadgets')], default='abstract', max_length=10)),
            ],
        ),
    ]

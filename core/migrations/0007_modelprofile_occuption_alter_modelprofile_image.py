# Generated by Django 5.1.2 on 2024-10-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_modelprofile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelprofile',
            name='occuption',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='modelprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
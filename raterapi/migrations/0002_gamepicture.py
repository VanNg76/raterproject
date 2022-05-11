# Generated by Django 4.0.4 on 2022-05-11 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('raterapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GamePicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_pic', models.ImageField(null=True, upload_to='actionimages')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='pictures', to='raterapi.game')),
            ],
        ),
    ]

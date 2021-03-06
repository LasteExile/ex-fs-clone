# Generated by Django 3.0.7 on 2020-06-20 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('motion_pictures', '0008_auto_20200619_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motionpicture',
            name='memberships',
            field=models.ManyToManyField(related_name='memmberships', to='motion_pictures.Membership'),
        ),
        migrations.RemoveField(
            model_name='motionpicture',
            name='rating',
        ),
        migrations.AddField(
            model_name='motionpicture',
            name='rating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='motion_pictures.Rating'),
        ),
    ]

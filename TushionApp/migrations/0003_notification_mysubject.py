# Generated by Django 5.0.6 on 2024-07-02 06:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TushionApp', '0002_student_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='mysubject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='TushionApp.mysubject'),
            preserve_default=False,
        ),
    ]

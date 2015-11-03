# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('related_date', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(to='tasks.Task')),
                ('user', models.ForeignKey(to='tasks.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='user',
            name='tasks',
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='task_list',
            field=models.ManyToManyField(to='tasks.Task', through='tasks.TaskUser'),
            preserve_default=True,
        ),
    ]

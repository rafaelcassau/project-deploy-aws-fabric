#coding: utf-8

from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_on']

    def __repr__(self):
        return '<Task: {}>'.format(self.title)

    def __unicode__(self):
        return '{}'.format(self.title)


class User(models.Model):
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    task_list = models.ManyToManyField(Task, through='TaskUser')

    class Meta:
        ordering = ['-created_at']

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def __unicode__(self):
        return '{}'.format(self.username)


class TaskUser(models.Model):
    task = models.ForeignKey(Task)
    user = models.ForeignKey(User)
    related_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('task', 'user')

    def __repr__(self):
        return '<task: {} - user: {}>'.format(task.title, user.username)

    def __unicode__(self):
        return '{}-{}'.format(self.task.title, self.user.username)
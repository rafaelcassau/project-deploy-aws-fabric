from django.db import models


class Task(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	posted_on = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		ordering = ['-posted_on']

	def __repr__(self):
		return '<Task: {}>'.format(self.title)

	def __unicode__(self):
		return 'Task: {}'.format(self.title)
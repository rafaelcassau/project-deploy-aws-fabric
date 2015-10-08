from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from tasks.models import Task


class TaskResource(DjangoResource):

	preparer = FieldsPreparer(fields={
		'id': 'id',
		'title': 'title',
		'description': 'description',
		'posted_on': 'posted_on'
	})

	def is_authenticated(self):
		return True

	# GET /api/tasks/
	def list(self):
		return Task.objects.all()

	# GET /api/tasks/<pk>/
	def detail(self, pk):
		return Task.objects.get(pk=pk)

	# POST /api/tasks/
	def create(self):
		return Task.objects.create(
			title=self.data['title'],
			description=self.data['description'],
		)

	# PUT /api/task/<pk>/
	def update(self, pk):
		try:
			task = Task.objects.get(pk=pk)
		except Task.DoesNotExist:
			task = Task()

		task.title = self.data['title']
		task.description = self.data['description']
		task.save()

		return task

	# DELETE /api/tasks/<pk>/
	def delete(self, pk):
		task = Task.objects.get(pk=pk).delete()
		return task




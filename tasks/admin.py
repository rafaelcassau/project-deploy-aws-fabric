#coding: utf-8

from django.contrib import admin
from .models import Task, User, TaskUser


class TaskAdminInline(admin.TabularInline):
	model = TaskUser
	extra = 1


class TaskAdmin(admin.ModelAdmin):
	
	date_hierarchy = 'posted_on'
	
	list_per_page = 10
	list_max_show_all = 1000

	fieldsets = (
		('Campos Obrigatórios', {
			'description': 'Neste Fieldset contem somente os campos obrigatórios',
			'fields': ('title', 'description', 'status'),
		}),
	)

	list_display = ('title', 'description', 'status', 'posted_on',)
	list_editable = ('status',)
	list_filter = ('title', 'status',)

	inlines = (TaskAdminInline,)


class UserAdmin(admin.ModelAdmin):
	
	date_hierarchy = 'created_at'
	
	list_per_page = 10
	list_max_show_all = 1000

	inlines = (TaskAdminInline,)

	list_display = ('username', 'created_at',)
	list_filter = ('username',)


admin.site.register(Task, TaskAdmin)
admin.site.register(User, UserAdmin)

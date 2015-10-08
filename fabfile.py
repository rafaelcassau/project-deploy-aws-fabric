from fabric.api import local, cd, run
import os


def run():
	local("./manage.py runserver 8000")

def execperm():
	local("sudo chmod +x manage.py")

def migrate():
	local("./manage.py makemigrations")
	local("./manage.py migrate")

def push(branch='master', message='add new features'):
	local_path = os.getcwd()
	with cd(local_path):
		local('git add .')
		local('git commit -m "{}"'.format(message))
		local("git push origin {} ".format(branch))

def prepare_deploy():
	local_path = '/opt/task_admin/'
	with cd(local_path):
		run('git checkout master')
		run('git pull origin master')

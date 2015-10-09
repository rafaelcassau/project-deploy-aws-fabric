from fabric.api import local, cd, run, env, sudo
import os

env.hosts = ['ec2-52-89-60-124.us-west-2.compute.amazonaws.com']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/rafaelcassau.pem'

def runserver():
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
	remote_path = '/opt/task_admin/'
	with cd(remote_path):
		sudo('git checkout master')
		sudo('git pull origin master')

def deploy():
	remote_path = '/opt/task_admin/'
	#run('workon task-admin')
	with cd(remote_path):
		run("python manage.py makemigrations")
		run("python manage.py migrate")	

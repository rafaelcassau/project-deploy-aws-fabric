#encoding: utf-8

from fabric.api import local, cd, run, env, prefix
import os

env.hosts = ['ec2-52-89-60-124.us-west-2.compute.amazonaws.com']
env.user = 'ubuntu'
env.key_filename = '~/rafaelcassau.pem'

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
	remote_path = '~/projects/task_admin/project/task_admin'
	with cd(remote_path):
		run('git checkout master')
		run('git pull origin master')

def deploy():
	"""
	É necessario adicionar as configurações da virtualenvwrapper no arquivo ".profile" e não
	no arquivo ".bashrc" pois a sessão ssh carrega as variaveis de contexto do ".profile" e não 
	do ".bashrc"
	"""
	run('workon task_admin')
	
	

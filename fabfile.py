from fabric.api import local

def run():
	local("./manage.py runserver 8000")

def execperm():
	local("sudo chmod +x manage.py")

def migrate():
	local("./manage.py makemigrations")
	local("./manage.py migrate")

def prepare_deploy():
	local("git add . && git commit")
	local("git push")
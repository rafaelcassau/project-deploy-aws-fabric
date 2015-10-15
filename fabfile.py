# encoding: utf-8

from fabric.api import local, cd, run, env

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

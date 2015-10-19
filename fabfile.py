# encoding: utf-8

from fabric.api import local, cd, run, env, sudo

env.hosts = ['ec2-52-89-60-124.us-west-2.compute.amazonaws.com']
env.user = 'ubuntu'
env.key_filename = '~/rafaelcassau.pem'


def runserver():
    local("./manage.py runserver 8000")


def execperm():
    local('sudo chmod +x manage.py')


def migrate():
    local("./manage.py makemigrations")
    local("./manage.py migrate")


def push(branch='master', message='Push features'):

    local_path = '~/projects/task_admin'

    with cd(local_path):
        local('git checkout {}'.format(branch))
        local('git add .')
        local('git commit -m "{}"'.format(message))
        local('git push origin {}'.format(branch))


def deploy(branch='master'):
    """
        É necessario adicionar as configurações da virtualenvwrapper no arquivo ".profile" e não
        no arquivo ".bashrc" pois a sessão ssh carrega as variaveis de contexto do ".profile" e não
        do ".bashrc"
    """
    remote_path = '~/projects/task_admin/task_admin/'

    with cd(remote_path):
        run('git checkout {}'.format(branch))
        run('git pull origin '.format(branch))
        run('workon task_admin')
        run('python manage.py migrate')

    sudo('/etc/init.d/supervisor stop')
    sudo('/etc/init.d/supervisor start task_admin')
    sudo('service nginx restart')





# encoding: utf-8

from fabric.api import local, cd, run, env, sudo, put
from fabric.context_managers import prefix

# Host settings
env.hosts = ['ec2-52-89-60-124.us-west-2.compute.amazonaws.com']
env.user = 'ubuntu'
env.key_filename = '~/rafaelcassau.pem'

# Project settings
env.project_name = 'task_admin'
env.project_port = '8000'
env.project_dns = 'ec2-52-89-60-124.us-west-2.compute.amazonaws.com'
env.github_project_url = 'https://github.com/rafaelcassau/task_admin.git'

env.local_path = '~/projects/{}'.format(env.project_name)

env.remote_root_path = '~/projects/'
env.remote_project_path = '~/projects/{}/'.format(env.project_name)
env.remote_project_source_path = '~/projects/{}/{}/'.format(env.project_name, env.project_name)

env.remote_virtualenv_path = '~/virtualenvs/'


def push(message='Push features', branch='master'):
    with cd(env.local_path):
        local('git checkout {}'.format(branch))
        local('git add .')
        local('git commit -m "{}"'.format(message))
        local('git push origin {}'.format(branch))


def bootstrap():
    """
        Considere o path da pasta projects já adicionado no /etc/nginx/nginx.conf
        Considere o path da pasta projects já adicionado no /etc/supervisord/supervisor.conf
        Considere a seguinte estrutura já existente:

       -- /home/<user>/
           -- projects/

        A task será responsavel por criar a estrutura completa do projeto especifico
        dentro do diretório <projects> informado acima.
    """
    create_project_structure()
    make_start_sh_conf()
    make_supervisor_conf()
    make_nginx_conf()

    clone()
    create_venv()
    deploy()


def create_project_structure():
    with cd(env.remote_root_path):
        run('mkdir -p {}/logs'.format(env.project_name))
        run('touch {}/logs/supervisor.log'.format(env.project_name))
        run('touch {}/logs/gunicorn.log'.format(env.project_name))
        run('touch {}/logs/access.log'.format(env.project_name))
        run('touch {}/logs/error.log'.format(env.project_name))
        run('mkdir -p {}/media'.format(env.project_name))
        run('mkdir -p {}/static'.format(env.project_name))


def create_venv():
    with cd(env.remote_virtualenv_path):
        run('mkvirtualenv {}'.format(env.project_name))

    with cd(env.remote_project_source_path), prefix('workon {}'.format(env.project_name)):
        run('pip install -r requirements/prod.txt')


def clone():
    with cd(env.remote_project_path):
        run('git clone {}'.format(env.github_project_url))


def kill_project():
    run('sudo service nginx stop')
    run('sudo service supervisor stop')
    run('rmvirtualenv {}'.format(env.project_name))

    with cd(env.remote_root_path):
        run('rm -rf {}'.format(env.project_name))


def deploy(branch='master'):
    """
        É necessario adicionar as configurações da virtualenvwrapper no arquivo ".profile" e não
        no arquivo ".bashrc" pois a sessão ssh carrega as variaveis de contexto do ".profile" e não
        do ".bashrc"
    """
    with cd(env.remote_project_source_path), prefix('workon {}'.format(env.project_name)):
        run('git checkout {}'.format(branch))
        run('git pull origin '.format(branch))
        run('pip install -r requirements_prod')
        run('python manage.py migrate')
        run('python manage.py collectstatic')

    sudo('/etc/init.d/supervisor stop')
    sudo('/etc/init.d/supervisor start task_admin')
    sudo('service nginx restart')

# ******** BUILDING TEMPLATE METHODS ********


def make_start_sh_conf():

    with open('start.sh', 'w') as start_sh:

        start_sh_template = _get_start_sh_template()

        start_sh_template = start_sh_template % {
            'user': env.user,
            'project_name': env.project_name,
            'project_port': env.project_port,
        }

        start_sh.write(start_sh_template)

    put('start.sh', env.remote_project_path)
    local('rm start.sh')

    with cd(env.remote_project_path):
        run('chmod +x start.sh')


def make_supervisor_conf():

    with open('supervisor.conf', 'w') as supervisor_conf:

        supervisor_template = _get_supervisor_template()

        supervisor_template = supervisor_template % {
            'user': env.user,
            'project_name': env.project_name,
        }
        supervisor_conf.write(supervisor_template)

    put('supervisor.conf', env.remote_project_path)
    local('rm supervisor.conf')


def make_nginx_conf():

    with open('nginx.conf', 'w') as nginx_conf:

        nginx_template = _get_nginx_template()

        nginx_template = nginx_template % {
            'project_dns': env.project_dns,
            'project_port': env.project_port,
            'user': env.user,
            'project_name': env.project_name,
        }
        nginx_conf.write(nginx_template)

    put('nginx.conf', env.remote_project_path)
    local('rm nginx.conf')


# ******** TEMPLATE METHODS ********

def _get_start_sh_template():

    start_sh_template = \
        '#!/bin/bash\n' \
        'set -e\n' \
        'LOGFILE=/home/%(user)s/projects/%(project_name)s/logs/gunicorn.log\n' \
        'LOGDIR=$(dirname $LOGFILE)\n' \
        'NUM_WORKERS=3\n' \
        'USER=%(user)s\n' \
        '#GROUP=root\n' \
        'ADDRESS=127.0.0.1:%(project_port)s\n' \
        'source /home/%(user)s/virtualenvs/%(project_name)s/bin/activate\n' \
        'cd /home/%(user)s/projects/%(project_name)s/%(project_name)s/\n' \
        'test -d $LOGDIR || mkdir -p $LOGDIR\n' \
        'exec gunicorn -w $NUM_WORKERS --bind=$ADDRESS --user=$USER --log-level=debug ' \
        '--log-file=$LOGFILE 2>>$LOGFILE %(project_name)s.wsgi:application'

    return start_sh_template


def _get_supervisor_template():

    supervisor_template = \
        '[program:%(project_name)s]\n' \
        'command=/home/%(user)s/projects/%(project_name)s/start.sh\n' \
        'user=%(user)s\n' \
        'stdout_logfile=/home/%(user)s/projects/%(project_name)s/logs/supervisor.log\n' \
        'redirect_stderr=true\n' \
        'autostart=true\n' \
        'autorestart=true'

    return supervisor_template


def _get_nginx_template():

    nginx_template = \
        'upstream %(project_dns)s {\n' \
        '    server 127.0.0.1:%(project_port)s;\n' \
        '}\n' \
        '\n' \
        'server {\n' \
        '    listen 80;\n' \
        '    server_name %(project_dns)s;\n' \
        '    client_max_body_size 50M;\n' \
        '\n' \
        '    access_log /home/%(user)s/projects/%(project_name)s/logs/access.log;\n' \
        '    error_log /home/%(user)s/projects/%(project_name)s/logs/error.log;\n' \
        '\n' \
        '    location /static/ {\n' \
        '        alias /home/%(user)s/projects/%(project_name)s/static/;\n' \
        '    }\n' \
        '    location /media/ {\n' \
        '        alias /home/%(user)s/projects/%(project_name)s/media/;\n' \
        '    }\n' \
        '    location / {\n' \
        '        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n' \
        '        proxy_set_header Host $http_host;\n' \
        '        proxy_redirect off;\n' \
        '\n' \
        '        if (!-f $request_filename) {\n' \
        '            proxy_pass http://%(project_dns)s;\n' \
        '            break;\n' \
        '        }\n' \
        '    }\n' \
        '}'

    return nginx_template




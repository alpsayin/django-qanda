from fabric.api import local

def prepare_deployment(branch_name):
    local('python manage.py test qanda_app')
    local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)

from fabric.api import lcd

def deploy():
    with lcd('/Users/alpsayin/Sites/qanda'):
        local('git pull /Users/alpsayin/qanda/')
        local('pip install django')
        local('pip install south')
        local('pip install fabric')
        # local('pip install django-taggit')
        local('git clone git://github.com/shacker/django-taggit.git')
        local('python django-taggit/setup.py install')
        local('pip install django-notify')
        local('pip install mysql-python')
        local('pip install django-extensions')
        local('pip install werkzeug')
        local('pip install django-tastypie')
        local('pip install django-debug-toolbar')
        local('pip install django-haystack')
        local('pip install pysolr')
        local('python manage.py validate')
        local('python manage.py syncdb')
        local('python manage.py migrate qanda_app')
        local('sudo apachectl stop && sudo apachectl start')

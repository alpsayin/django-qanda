from fabric.api import local

def prepare_deployment(branch_name):
    local('python manage.py test qanda_app')
    local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)

from fabric.api import lcd

def deploy():
    with lcd('/Users/alpsayin/Sites/qanda'):
        local('git pull /Users/alpsayin/qanda/')
        local('python manage.py migrate qanda_app')
        local('python manage.py test qanda_app')
        local('sudo apachectl stop && sudo apachectl start')

#!/bin/sh

source ./env/bin/activate
pip install django==1.4.3
pip install south
pip install fabric
# pip install django-taggit
git clone git://github.com/alpsayin/django-taggit.git
python django-taggit/setup.py install
pip install django-notify
pip install mysql-python
pip install django-extensions
pip install werkzeug
pip install django-tastypie
pip install django-haystack
pip install django-userena
pip install pysolr
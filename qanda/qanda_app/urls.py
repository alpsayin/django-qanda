from django.conf.urls import patterns, include, url
from django.conf.urls import patterns
from views import question_page, new_question_page, question_relation_submit, subscription_submit, most_recent_question, question_list, tag_page
from tastypie.api import Api
from api import UserResource, QandaUserResource, QuestionResource, AnswerResource, ReplyResource
from django_notify.urls import get_pattern as get_notify_pattern

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(QandaUserResource())
v1_api.register(QuestionResource())
v1_api.register(AnswerResource())
v1_api.register(ReplyResource())

urlpatterns = patterns('qanda_app',
    url(r'^$', 'views.index', name='index'),
    url(r'^new/$', new_question_page, name='new_question_page'),
    url(r'^last/$', most_recent_question, name='most_recent_question'),
    url(r'^list/(?P<question_id>\d+)/$', question_list, name='question_list'),
    url(r'^tag/(?P<tag>\w+)/(?P<page>\d+)$', tag_page, name='tag_page'),
    url(r'^(?P<question_id>\d+)/$', question_page, name='question_page'),
    url(r'^(?P<question_id>\d+)/relate/$', question_relation_submit, name='question_relation_submit'),
    url(r'^(?P<question_id>\d+)/subscribe/$', subscription_submit, name='subscription_submit'),

    #django_notify
    (r'^notify/', get_notify_pattern()),

    #api
    (r'^api/', include(v1_api.urls)),

)
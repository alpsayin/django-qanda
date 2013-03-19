from django.conf.urls import patterns, include, url
from django.conf.urls import patterns
from views import question_page
from views import new_question_page
from views import edit_question_page
from views import delete_answer
from views import question_relation_submit
from views import subscription_submit
from views import most_recent_question
from views import question_list
from views import tag_page
from views import categorized_tag_page
from views import tag_list
from views import relate_answer_single
from views import relate_question_single
from views import subscribe_question
from views import subscribe_answer
from views import login_redirect
from views import searchdoc
from views import category_list
from views import profile_page
from views import user_asked_questions_list
from views import user_answered_questions_list
from views import user_replied_questions_list
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
    url(r'^qanda-login-redirect/(?P<redirect_url>.+)$', login_redirect, name='login_redirect'),
    url(r'^new/$', new_question_page, name='new_question_page'),
    url(r'^edit/(?P<question_id>\d+)/$', edit_question_page, name='edit_question_page'),
    url(r'^answer/(?P<answer_id>\d+)/delete/$', delete_answer, name='delete_answer'),
    url(r'^answer/(?P<answer_id>\d+)/edit/$', delete_answer, name='delete_answer'),
    url(r'^last/$', most_recent_question, name='most_recent_question'),
    url(r'^list/(?P<question_id>\d+)/$', question_list, {'category' : 'all'}, name='question_list'),
    url(r'^list/(?P<question_id>\d+)/(?P<category>\w+)/$', question_list, name='categorized_question_list'),
    url(r'^tag/(?P<tag>\w+)/(?P<page>\d+)$', tag_page, name='tag_page'),
    url(r'^(?P<category>\w+)/tag/(?P<tag>\w+)/(?P<page>\d+)$', categorized_tag_page, name='categorized_tag_page'),
    url(r'^tags/(?P<page>\d+)/$', tag_list, name='tag_list'),
    url(r'^categories/(?P<page>\d+)/$', category_list, name='category_list'),
    url(r'^user/(?P<user_id>\d+)/$', profile_page, name='profile_page'),
    url(r'^user/(?P<user_id>\d+)/asked/(?P<question_id>\d+)/$', user_asked_questions_list, {'category' : 'all'}, name='user_asked_questions_list'),
    url(r'^user/(?P<user_id>\d+)/asked/(?P<question_id>\d+)/(?P<category>\w+)/$', user_asked_questions_list, name='categorized_user_asked_questions_list'),
    url(r'^user/(?P<user_id>\d+)/answered/(?P<question_id>\d+)/$', user_answered_questions_list, {'category' : 'all'}, name='user_answered_questions_list'),
    url(r'^user/(?P<user_id>\d+)/answered/(?P<question_id>\d+)/(?P<category>\w+)/$', user_answered_questions_list, name='categorized_user_answered_questions_list'),
    url(r'^user/(?P<user_id>\d+)/replied/(?P<question_id>\d+)/$', user_replied_questions_list, { 'category' : 'all'}, name='user_replied_questions_list'),
    url(r'^user/(?P<user_id>\d+)/replied/(?P<question_id>\d+)/(?P<category>\w+)/$', user_replied_questions_list, name='categorized_user_replied_questions_list'),
    url(r'^(?P<question_id>\d+)/$', question_page, name='question_page'),
    url(r'^(?P<question_id>\d+)/searchdoc$', searchdoc, name='searchdoc'),
    url(r'^(?P<question_id>\d+)/(?P<answer_id>\d+)/subscribe/(?P<value>.+)/$', subscribe_answer, name='subscribe_answer'),
    url(r'^(?P<question_id>\d+)/subscribe/(?P<value>.+)/$', subscribe_question, name='subscribe_question'),
    url(r'^(?P<question_id>\d+)/relate_single/(?P<relation>.+)/(?P<value>.+)/$', relate_question_single, name='relate_question_single'),
    url(r'^(?P<question_id>\d+)/(?P<answer_id>\d+)/(?P<relation>.+)/(?P<value>.+)/$', relate_answer_single, name='relate_answer_single'),
    url(r'^(?P<question_id>\d+)/relate/$', question_relation_submit, name='question_relation_submit'),
    url(r'^(?P<question_id>\d+)/subscribe/$', subscription_submit, name='subscription_submit'),

    #django_notify
    (r'^notify/', get_notify_pattern()),

    #api
    (r'^api/', include(v1_api.urls)),

)
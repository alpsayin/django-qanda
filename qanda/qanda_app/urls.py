from django.conf.urls import patterns, include, url
from django.conf.urls import patterns
from views import question_page

from tastypie.api import Api
from api import UserResource, QandaUserResource, QuestionResource, AnswerResource, ReplyResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(QandaUserResource())
v1_api.register(QuestionResource())
v1_api.register(AnswerResource())
v1_api.register(ReplyResource())

urlpatterns = patterns('qanda_app',
    url(r'^$', 'views.index', name='index'),
    url(r'^(?P<question_id>\d+)/$', question_page, name='question_page'),

    #api
    (r'^api/', include(v1_api.urls)),

)
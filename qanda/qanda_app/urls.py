from django.conf.urls import patterns, include, url
from django.conf.urls import patterns
from views import QuestionView

urlpatterns = patterns('qanda_app',
    url(r'^$', 'views.index', name='index'),
    url(r'^(?P<question_id>\d+)/$', QuestionView.as_view(), name='question_page'),
)
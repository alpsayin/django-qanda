# Create your views here.
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.contrib import auth
from django.shortcuts import redirect
from django.template.context import RequestContext

from models import *

def get_user(request):
	if not hasattr(request, '_cached_user'):
		request._cached_user = auth.get_user(request)
	return request._cached_user

def index(request):
	return HttpResponse("questions index")

def question_page(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	if request.method == 'POST':
		if request.POST['type'] == 'question' and request.POST['pk'] == str(question.pk):
			if 'star' in request.POST:
				Question.objects.star(get_user(request), question)
			else:
				Question.objects.unstar(get_user(request), question)
			if 'flag' in request.POST:
				Question.objects.flag(get_user(request), question)
			else:
				Question.objects.unflag(get_user(request), question)
			if 'upvote' in request.POST:
				Question.objects.upvote(get_user(request), question)
			else:
				Question.objects.unupvote(get_user(request), question)
			if 'downvote' in request.POST:
				Question.objects.downvote(get_user(request), question)
			else:
				Question.objects.undownvote(get_user(request), question)
			if 'useful' in request.POST:
				Question.objects.useful(get_user(request), question)
			else:
				Question.objects.unuseful(get_user(request), question)
			if 'notUseful' in request.POST:
				Question.objects.notUseful(get_user(request), question)
			else:
				Question.objects.unnotUseful(get_user(request), question)
		elif request.POST['type'] == 'answer':
			if 'star' in request.POST:
				Answer.objects.star(get_user(request).QandaUser, Answer.objects.get(pk=int(request.POST['pk'])))
			else:
				Answer.objects.unstar(get_user(request).QandaUser, Answer.objects.get(pk=int(request.POST['pk'])))
			if 'flag' in request.POST:
				Answer.objects.flag(get_user(request).QandaUser, Answer.objects.get(pk=int(request.POST['pk'])))
			else:
				Answer.objects.unflag(get_user(request).QandaUser, Answer.objects.get(pk=int(request.POST['pk'])))
			if 'upvote' in request.POST:
				Answer.objects.upvote(get_user(request).QandaUser, Answer.objects.get(pk=int(request.POST['pk'])))
			else:
				Answer.objects.unupvote(get_user(request).QandaUser, Answer.objects.get(pk=int(request.POST['pk'])))
			if 'downvote' in request.POST:
				Answer.objects.downvote(get_user(request).QandaUser, Answer.objects.get(pk=int(request.POST['pk'])))
			else:
				Answer.objects.undownvote(get_user(request).QandaUser, Answer.objects.get(pk=int(request.POST['pk'])))
			if 'useful' in request.POST:
				Answer.objects.useful(get_user(request).QandaUser, Answer.objects.get(pk=int(request.POST['pk'])))
			else:
				Answer.objects.unuseful(get_user(request).QandaUser, Answer.objects.get(pk=int(request.POST['pk'])))
			if 'notUseful' in request.POST:
				Answer.objects.notUseful(get_user(request).QandaUser, Answer.objects.get(pk=int(request.POST['pk'])))
			else:
				Answer.objects.unnotUseful(get_user(request).QandaUser, Answer.objects.get(pk=int(request.POST['pk'])))
	question = get_object_or_404(Question, pk=question_id)
	answers = question.answers.all()
	context = {}
	context['question'] = question
	question.relations = QuestionRelatedUsers.objects.filter(relatedQuestion=question, relatedUser__djangoUser=get_user(request))[0]
	for answer in answers:
		if AnswerRelatedUsers.objects.filter(relatedAnswer=answer, relatedUser__djangoUser=get_user(request)).count():
			answer.relations = AnswerRelatedUsers.objects.filter(relatedAnswer=answer, relatedUser__djangoUser=get_user(request))[0]

	context['answers'] = answers
	context['debug'] = ''
	return render_to_response('question.html', context, context_instance=RequestContext(request))


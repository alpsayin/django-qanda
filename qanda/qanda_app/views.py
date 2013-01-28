# Create your views here.
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.contrib import auth
from django.shortcuts import redirect
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from forms import QuestionForm, AnswerForm, ReplyForm

from models import *

def get_user(request):
	if not hasattr(request, '_cached_user'):
		request._cached_user = auth.get_user(request)
	return request._cached_user

def index(request):
	return HttpResponseRedirect(reverse(question_page, args=(Question.objects.count(),)))

def process_question_relations(request, question, qandaUser):
	relation_types = ['star', 'flag', 'upvote', 'downvote', 'useful', 'notUseful']
	relations = dict()
	for submitted_key in request.POST:
		if submitted_key in relation_types:
			relations[submitted_key] = True
	for relation_type in relation_types:
		if relation_type not in relations:
			relations[relation_type] = False
	Question.objects.set_relations(qandaUser, question, relations)

def process_answer_relations(request, answer, qandaUser):
	relation_types = ['star', 'flag', 'upvote', 'downvote', 'useful', 'notUseful']
	relations = dict()
	for submitted_key in request.POST:
		if submitted_key in relation_types:
			relations[submitted_key] = True
	for relation_type in relation_types:
		if relation_type not in relations:
			relations[relation_type] = False
	Answer.objects.set_relations(qandaUser, answer, relations)

def process_new_answer(answer_form, question, qandaUser):
	"""
		Process a new answer
	"""
	answer = answer_form.save(commit=False)
	answer.question = question
	answer.author = qandaUser
	answer.save()
	answer_form.save_m2m()
	return answer

def process_new_reply(reply_form, answer, qandaUser):
	"""
		Process a new reply
	"""
	reply = reply_form.save(commit=False)
	reply.answer = answer
	reply.author = qandaUser
	reply.save()
	reply_form.save_m2m()
	return reply

def process_new_question(question_form, qandaUser):
	"""
		Process a new question
	"""
	question = question_form.save(commit=False)
	question.author = qandaUser
	question.viewCount = 0
	question.save()
	question_form.save_m2m()
	return question

@login_required(login_url='/admin/', redirect_field_name='next')
def new_question_page(request):
	if request.method == 'POST':
		if request.POST['type'] == 'new_question':
			question_form = QuestionForm(request.POST)
			if question_form.is_valid():
				qandaUser = get_user(request).QandaUser
				question = process_new_question(question_form, qandaUser)
				return HttpResponseRedirect(reverse(question_page, args=(question.pk,)))
	context = {}
	context['type'] = 'new_question'
	context['question_form'] = QuestionForm()
	return render_to_response("new_question.html", context, context_instance=RequestContext(request))

@login_required(login_url='/admin/', redirect_field_name='next')
def question_relation_submit(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	user = get_user(request)
	if request.user.is_authenticated():
		if request.method == 'POST':
			qandaUser = user.QandaUser
			if request.POST['type'] == 'question' and request.POST['pk'] == str(question.pk):
				process_question_relations(request, question, qandaUser)
			elif request.POST['type'] == 'answer':
				answer = Answer.objects.get(pk=int(request.POST['pk']))
				print answer
				process_answer_relations(request, answer, qandaUser)
			elif request.POST['type'] == 'new_answer':
				answer_form = AnswerForm(request.POST)
				if answer_form.is_valid():
					process_new_answer(answer_form, question, qandaUser)
			elif request.POST['type'] == 'new_reply':
				answer = Answer.objects.get(pk=int(request.POST['pk']))
				reply_form = ReplyForm(request.POST)
				if reply_form.is_valid():
					process_new_reply(reply_form, answer, qandaUser)
			elif request.POST['type'] == 'new_question':
				process_new_question(request, qandaUser)

	return HttpResponseRedirect(reverse(question_page, args=(Question.objects.count(),)))


def question_page(request, question_id):
	context = {}
	question = get_object_or_404(Question, pk=question_id)
	if request.user.is_authenticated():
		all_relations = QuestionRelatedUsers.objects.filter(relatedQuestion=question, relatedUser__djangoUser=get_user(request))
		if all_relations.count() > 0: 
			question.relations = all_relations[0]
			
	answers = question.answers.filter(deleted=False)
	if request.user.is_authenticated():
		for answer in answers:
			if AnswerRelatedUsers.objects.filter(relatedAnswer=answer, relatedUser__djangoUser=get_user(request)).count():
				answer.relations = AnswerRelatedUsers.objects.filter(relatedAnswer=answer, relatedUser__djangoUser=get_user(request))[0]
	context['question'] = question
	context['answers'] = answers
	context['debug'] = ''
	context['answer_form'] = AnswerForm()
	context['reply_form'] = ReplyForm()

	Question.objects.increment_view_count(question)
	return render_to_response('question.html', context, context_instance=RequestContext(request))


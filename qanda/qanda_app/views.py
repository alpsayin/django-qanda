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
from forms import QuestionForm, AnswerForm, ReplyForm, SubscriptionForm
from taggit.models import Tag
import pprint

from decorators import assert_qanda_user
from models import *

NUM_OF_QUESTIONS_PER_PAGE = 10
NUM_OF_TAGS_PER_PAGE = 60
NUM_OF_TAGS_IN_COMMON_TAGS = 16
NUM_OF_TAGS_IN_RECENT_TAGS = 16

def get_user(request):
	if not hasattr(request, '_cached_user'):
		request._cached_user = auth.get_user(request)
	return request._cached_user

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

@assert_qanda_user
def index(request):
	try:
		latest_question = Question.objects.latest('postDate')
		return HttpResponseRedirect(reverse(question_list, args=(latest_question.pk,)))
	except:
		return HttpResponseRedirect(reverse(new_question_page, args=()))

@assert_qanda_user
def question_list(request, question_id):
	context = {}
	questions = Question.objects.filter(pk__lte=question_id).order_by('-postDate')[:NUM_OF_QUESTIONS_PER_PAGE]
	for question in questions:
		question.voteCount = QuestionRelatedUsers.objects.filter(relatedQuestion=question, upvote=True).count
	context['questions'] = questions
	context['view'] = 'question_list'

	next_qset = Question.objects.filter(pk__lte=int(question_id)+NUM_OF_QUESTIONS_PER_PAGE).order_by('-postDate')[:1]
	if next_qset[0].pk > int(question_id):
		context['next'] = int(question_id)+NUM_OF_QUESTIONS_PER_PAGE

	prev_qset = Question.objects.filter(pk__lte=int(question_id)-NUM_OF_QUESTIONS_PER_PAGE).order_by('-postDate')[:1]
	if prev_qset.exists():
		context['prev'] = prev_qset[0].pk

	context['recent_tags'] = Tag.objects.order_by('-pk').all()[:NUM_OF_TAGS_IN_RECENT_TAGS]
	context['common_tags'] = Question.tags.most_common()[:NUM_OF_TAGS_IN_COMMON_TAGS]

	return render_to_response("question_list.html", context, context_instance=RequestContext(request))

@assert_qanda_user
def tag_list(request, page):
	context = {}
	page = int(page)
	
	tags = Tag.objects.order_by('name')[page*(NUM_OF_TAGS_PER_PAGE):(page+1)*NUM_OF_TAGS_PER_PAGE]
	for tag in tags:
		tag.count = Question.objects.filter(tags__name__in=[tag]).count()

	context['tags'] = tags
	context['view'] = 'tag_list'

	next_qset = Tag.objects.order_by('name')[(page+1)*NUM_OF_TAGS_PER_PAGE:(page+2)*NUM_OF_TAGS_PER_PAGE]
	if next_qset.exists():
		context['next'] = page+1

	if page >= 1:
		prev_qset = Tag.objects.order_by('name')[(page-1)*NUM_OF_TAGS_PER_PAGE:page*NUM_OF_TAGS_PER_PAGE]
		if prev_qset.exists():
			context['prev'] = page-1


	return render_to_response("tag_list.html", context, context_instance=RequestContext(request))


@assert_qanda_user
def tag_page(request, tag, page):
	context = {}
	page = int(page)
	questions = Question.objects.filter(tags__name__in=[tag]).order_by('-postDate')[page*(NUM_OF_QUESTIONS_PER_PAGE):(page+1)*NUM_OF_QUESTIONS_PER_PAGE]
	for question in questions:
		question.voteCount = QuestionRelatedUsers.objects.filter(relatedQuestion=question, upvote=True).count
	context['questions'] = questions
	context['tag'] = tag
	context['view'] = 'tag_page'

	next_qset = Question.objects.filter(tags__name__in=[tag]).order_by('-postDate')[(page+1)*NUM_OF_QUESTIONS_PER_PAGE:(page+2)*NUM_OF_QUESTIONS_PER_PAGE]
	if next_qset.exists():
		context['next'] = page+1

	if page >= 1:
		prev_qset = Question.objects.filter(tags__name__in=[tag]).order_by('-postDate')[(page-1)*NUM_OF_QUESTIONS_PER_PAGE:page*NUM_OF_QUESTIONS_PER_PAGE]
		if prev_qset.exists():
			context['prev'] = page-1

	context['recent_tags'] = Tag.objects.order_by('-pk').all()[:NUM_OF_TAGS_IN_RECENT_TAGS]
	context['common_tags'] = Question.tags.most_common()[:NUM_OF_TAGS_IN_COMMON_TAGS]

	return render_to_response("tag_page.html", context, context_instance=RequestContext(request))

@assert_qanda_user
def most_recent_question(request):
	try:
		latest_question = Question.objects.latest('postDate')
		return HttpResponseRedirect(reverse(question_page, args=(latest_question.pk,)))
	except:
		return HttpResponseRedirect(reverse(new_question_page, args=()))

@assert_qanda_user
@login_required
def new_question_page(request):
	context = {}
	context['type'] = 'new_question'

	if request.method == 'POST':
		if request.POST['type'] == 'new_question':
			question_form = QuestionForm(request.POST)
			context['question_form'] = question_form
			if question_form.is_valid():
				qandaUser = get_user(request).QandaUser
				question = process_new_question(question_form, qandaUser)
				return HttpResponseRedirect(reverse(question_page, args=(question.pk,)))
	else:
		context['question_form'] = QuestionForm()

	context['view'] = 'new_question_page'
	context['debug'] = ''
	return render_to_response("new_question.html", context, context_instance=RequestContext(request))

@assert_qanda_user
@login_required
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

	return HttpResponseRedirect(reverse(question_page, args=(question.pk,)))

@assert_qanda_user
@login_required
def subscription_submit(request, **kwargs):
	question = get_object_or_404(Question, pk=kwargs['question_id'])
	user = get_user(request)
	if request.user.is_authenticated():
		if request.method == 'POST':
			qandaUser = user.QandaUser
			if request.POST['type'] == 'question_subscription' and request.POST['pk'] == str(question.pk):
				if 'subscribed' in request.POST:
					subscribed = True
				else:
					subscribed = False
				Question.objects.subscribe_to_question(question, qandaUser, subscribed)
			if request.POST['type'] == 'answer_subscription':
				answer = get_object_or_404(Answer, pk=request.POST['pk'])
				if 'subscribed' in request.POST:
					subscribed = True
				else:
					subscribed = False
				Answer.objects.subscribe_to_answer(answer, qandaUser, subscribed)

	return HttpResponseRedirect(reverse(question_page, args=(question.pk,)))

def question_page(request, question_id):
	context = {}
	if not Question.objects.exists():
		context = {}
		context['type'] = 'new_question'
		context['question_form'] = QuestionForm()
		return HttpResponseRedirect(reverse(new_question_page, args=()))
	question = get_object_or_404(Question, pk=question_id)
	user = get_user(request)
	if request.user.is_authenticated():
		all_relations = QuestionRelatedUsers.objects.filter(relatedQuestion=question, relatedUser__djangoUser=get_user(request))
		if all_relations.count() > 0: 
			question.relations = all_relations[0]
			
	answers = question.answers.filter(deleted=False)
	if request.user.is_authenticated():
		for answer in answers:
			if AnswerRelatedUsers.objects.filter(relatedAnswer=answer, relatedUser__djangoUser=get_user(request)).count():
				answer.relations = AnswerRelatedUsers.objects.filter(relatedAnswer=answer, relatedUser__djangoUser=get_user(request))[0]

			try:
				subscription = AnswerSubscription.objects.get(settings__user=user, answer=answer)
				if subscription:
					answer.subscribed = 'True'
			except:
				pass


		context['subscription_form'] = SubscriptionForm({'subscribed':False,})
		try:
			subscription = QuestionSubscription.objects.get(settings__user=user, question=question)
			if subscription:
				question.subscribed = 'True'
		except:
			pass

		context['answer_form'] = AnswerForm()
		context['reply_form'] = ReplyForm()

	context['question'] = question
	context['answers'] = answers
	context['debug'] = ''

	if question == Question.objects.latest('pk'):
		context['view'] = 'last_question_page'
	else:
		context['view'] = 'question_page'

		
	context['recent_tags'] = Tag.objects.order_by('-pk').all()[:NUM_OF_TAGS_IN_RECENT_TAGS]
	context['common_tags'] = Question.tags.most_common()[:NUM_OF_TAGS_IN_COMMON_TAGS]

	Question.objects.increment_view_count(question)
	return render_to_response('question.html', context, context_instance=RequestContext(request))


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
from view_helpers import *
import pprint

from decorators import assert_qanda_user
from models import *

NUM_OF_QUESTIONS_PER_PAGE = 10
NUM_OF_TAGS_PER_PAGE = 70
NUM_OF_TAGS_IN_COMMON_TAGS = 16
NUM_OF_TAGS_IN_RECENT_TAGS = 16
NUM_OF_TAGS_IN_COMMON_TAGS_IN_TAG_LIST = 10
NUM_OF_TAGS_IN_RECENT_TAGS_IN_TAG_LIST = 10

# FORM PROCESSORS

@assert_qanda_user
@login_required
def subscribe_question(request, question_id, value):
	value = value == 'true'
	question = get_object_or_404(Question, pk=question_id)
	user = get_user(request)
	if request.user.is_authenticated():
		qandaUser = user.QandaUser
		Question.objects.subscribe_to_question(question, qandaUser, value)
	return HttpResponseRedirect(reverse(question_page, args=(question_id,)))

@assert_qanda_user
@login_required
def subscribe_answer(request, question_id, answer_id, value):
	value = value == 'true'
	answer = get_object_or_404(Answer, pk=answer_id)
	question = get_object_or_404(Question, pk=question_id)
	user = get_user(request)
	if request.user.is_authenticated():
		if answer in question.answers.all():
			qandaUser = user.QandaUser
			Answer.objects.subscribe_to_answer(answer, qandaUser, value)
	return HttpResponseRedirect(reverse(question_page, args=(question_id,)))

@assert_qanda_user
@login_required
def relate_question_single(request, question_id, relation, value):
	question = get_object_or_404(Question, pk=question_id)
	user = get_user(request)
	if request.user.is_authenticated():
		qandaUser = user.QandaUser
		relation_types = ['star', 'flag', 'upvote', 'downvote', 'useful', 'notUseful']
		relations = dict()
		relations[relation] = value=='true'
		Question.objects.set_relations(qandaUser, question, relations)
	return HttpResponseRedirect(reverse(question_page, args=(question_id,)))

@assert_qanda_user
@login_required
def relate_answer_single(request, question_id, answer_id, relation, value):
	answer = get_object_or_404(Answer, pk=answer_id)
	question = get_object_or_404(Question, pk=question_id)
	user = get_user(request)
	if request.user.is_authenticated():
		if answer in question.answers.all():
			qandaUser = user.QandaUser
			relation_types = ['star', 'flag', 'upvote', 'downvote', 'useful', 'notUseful']
			relations = dict()
			relations[relation] = value=='true'
			Answer.objects.set_relations(qandaUser, answer, relations)
	return HttpResponseRedirect(reverse(question_page, args=(answer.question.pk,)))

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

# INDEX PAGES

@login_required
@assert_qanda_user
def login_redirect(request, redirect_url):
	return HttpResponseRedirect(redirect_url)

@assert_qanda_user
def index(request):
	return HttpResponseRedirect(reverse(question_list, args=(0,)))

@assert_qanda_user
def searchdoc(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	context = {}
	context['object'] = question
	return render_to_response('search/indexes/qanda_app/question_text.txt', context, context_instance=RequestContext(request))

@assert_qanda_user
def question_list(request, question_id):
	context = {}
	if int(question_id) <= 0:
		try:
			question_id = Question.objects.latest('pk').pk
		except:
			pass

	questions = Question.objects.filter(pk__lte=question_id).order_by('-postDate')[:NUM_OF_QUESTIONS_PER_PAGE]
	for question in questions:
		question.voteCount = QuestionRelatedUsers.objects.filter(relatedQuestion=question, upvote=True).count() - QuestionRelatedUsers.objects.filter(relatedQuestion=question, downvote=True).count()
	context['questions'] = questions
	context['view'] = 'question_list'

	next_qset = Question.objects.filter(pk__lte=int(question_id)+NUM_OF_QUESTIONS_PER_PAGE).order_by('-postDate')[:1]
	if next_qset.exists():
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

	context['recent_tags'] = Tag.objects.order_by('-pk').all()[:NUM_OF_TAGS_IN_RECENT_TAGS_IN_TAG_LIST]
	context['common_tags'] = Question.tags.most_common()[:NUM_OF_TAGS_IN_COMMON_TAGS_IN_TAG_LIST]

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

	context['recent_tags'] = Tag.objects.order_by('-pk').all()[:NUM_OF_TAGS_IN_RECENT_TAGS]
	context['common_tags'] = Question.tags.most_common()[:NUM_OF_TAGS_IN_COMMON_TAGS]

	return render_to_response("new_question.html", context, context_instance=RequestContext(request))


def question_page(request, question_id):
	context = {}
	if not Question.objects.exists():
		context = {}
		context['type'] = 'new_question'
		context['question_form'] = QuestionForm()
		return HttpResponseRedirect(reverse(new_question_page, args=()))
	question = get_object_or_404(Question, pk=question_id)
	question.numOfVotes = QuestionRelatedUsers.objects.filter(relatedQuestion=question, upvote=True).count() - QuestionRelatedUsers.objects.filter(relatedQuestion=question, downvote=True).count()
	user = get_user(request)
	if request.user.is_authenticated():
		all_relations = QuestionRelatedUsers.objects.filter(relatedQuestion=question, relatedUser__djangoUser=get_user(request))
		if all_relations.count() > 0: 
			question.relations = all_relations[0]
			
	answers = question.answers.filter(deleted=False)
	if user.is_authenticated():
		relations = question.user_relation.filter(relatedUser=user.QandaUser)
		if relations.exists():
			relations = relations[0]
			question.relations = relations
		for answer in answers:
			answer.numOfVotes = AnswerRelatedUsers.objects.filter(relatedAnswer=answer, upvote=True).count() - AnswerRelatedUsers.objects.filter(relatedAnswer=answer, downvote=True).count()
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

	try:
		if question == Question.objects.latest('pk'):
			context['view'] = 'last_question_page'
		else:
			context['view'] = 'question_page'
	except:
		context['view'] = 'question_page'



	context['recent_tags'] = Tag.objects.order_by('-pk').all()[:NUM_OF_TAGS_IN_RECENT_TAGS]
	context['common_tags'] = Question.tags.most_common()[:NUM_OF_TAGS_IN_COMMON_TAGS]

	Question.objects.increment_view_count(question)
	return render_to_response('question.html', context, context_instance=RequestContext(request))


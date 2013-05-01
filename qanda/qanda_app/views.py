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
from forms import QuestionForm, AnswerForm, ReplyForm, SubscriptionForm, QuestionCloseForm, CategoryForm
from taggit.models import Tag
from django.http import Http404
from django.conf import settings
from django.template.defaultfilters import slugify
from view_helpers import *
import pprint
import random

from decorators import assert_qanda_user
from models import *

NUM_OF_QUESTIONS_PER_PAGE = 8
NUM_OF_TAGS_PER_PAGE = 70

##############################################
#
# FORM PROCESSORS
#
##############################################

@assert_qanda_user
@login_required
def subscribe_question(request, question_id, value):
	value = value == 'true'
	question = get_object_or_404(Question, pk=question_id)
	if not question.deleted or not question.closed:
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
	if not question.deleted or not question.closed:
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
	if not question.deleted or not question.closed:
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
	if not question.deleted or not question.closed:
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
	if not question.deleted or not question.closed:
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
	if not question.deleted or not question.closed:
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



##############################################
#
# EDITOR VIEWS
#
##############################################

@login_required
@assert_qanda_user
def add_category(request):
	random_slug_chars = ['_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',]
	user = get_user(request)
	if user.is_superuser or user.groups.filter(name=getattr(settings, 'QANDA_EDITORS_GROUP_NAME', 'Editors')).exists():
		if request.method == 'POST':
			category_form = CategoryForm(request.POST)
			if category_form.is_valid():
				newCategory = category_form.save(commit=False)
				encodedName = newCategory.name
				encodedName = encodedName.replace(u'\u0130', u'I')
				encodedName = encodedName.replace(u'\u0131', u'i')
				encodedName = encodedName.replace(u'\u00D6', u'O')
				encodedName = encodedName.replace(u'\u00F6', u'o')
				encodedName = encodedName.replace(u'\u00DC', u'U')
				encodedName = encodedName.replace(u'\u00FC', u'u')
				encodedName = encodedName.replace(u'\u00C7', u'C')
				encodedName = encodedName.replace(u'\u00E7', u'c')
				encodedName = encodedName.replace(u'\u011E', u'G')
				encodedName = encodedName.replace(u'\u011F', u'g')
				encodedName = encodedName.replace(u'\u015E', u'S')
				encodedName = encodedName.replace(u'\u015F', u's')
				temp_slug = slugify(encodedName) 
				temp_slug = temp_slug.replace('-', '_')
				while Category.objects.filter(slug=temp_slug).exists():
					temp_slug = temp_slug + random_slug_chars[random.randint(0, len(random_slug_chars))]
				newCategory.slug = temp_slug
				newCategory.save()
	return HttpResponseRedirect(reverse(category_list, args=(0,)))


@login_required
@assert_qanda_user
def close_question_page(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	if not question.deleted:
		user = get_user(request)
		if user  == question.author.djangoUser or user.is_superuser or user.groups.filter(name=getattr(settings, 'QANDA_EDITORS_GROUP_NAME', 'Editors')).exists():
			if request.method == 'POST':
				question_close_form = QuestionCloseForm(request.POST)
				if question_close_form.is_valid():
					question.closeMessage = question_close_form.cleaned_data['message']
			question.closed = True
			question.save()
		return HttpResponseRedirect(reverse(question_page, args=(question.pk,)))
	else:
		return HttpResponseRedirect(reverse(question_list, args=(0,)))

@login_required
@assert_qanda_user
def delete_question(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	user = get_user(request)
	if user  == question.author.djangoUser or user.is_superuser or user.groups.filter(name=getattr(settings, 'QANDA_EDITORS_GROUP_NAME', 'Editors')).exists():
		question.deleted = True
		question.save()
	return HttpResponseRedirect(reverse(question_list, args=(0,)))

@login_required
@assert_qanda_user
def edit_answer_page(request, answer_id):
	answer = get_object_or_404(Answer, pk=answer_id)
	question = answer.question
	if not question.deleted or not question.closed:
		user = get_user(request)
		if user  == answer.author.djangoUser or user.is_superuser or user.groups.filter(name=getattr(settings, 'QANDA_EDITORS_GROUP_NAME', 'Editors')).exists():
			print 'function call: edit_question'
	return HttpResponseRedirect(reverse(question_page, args=(answer.question.pk,)))

@login_required
@assert_qanda_user
def delete_answer(request, answer_id):
	answer = get_object_or_404(Answer, pk=answer_id)
	question = answer.question
	if not question.deleted or not question.closed:
		user = get_user(request)
		if user  == answer.author.djangoUser or user.is_superuser or user.groups.filter(name=getattr(settings, 'QANDA_EDITORS_GROUP_NAME', 'Editors')).exists():
			answer.deleted = True
			answer.save()
	return HttpResponseRedirect(reverse(question_page, args=(answer.question.pk,)))

@login_required
@assert_qanda_user
def delete_reply(request, reply_id):
	reply = get_object_or_404(Reply, pk=reply_id)
	question = reply.answer.question
	if not question.deleted or not question.closed:
		user = get_user(request)
		if user  == reply.author.djangoUser or user.is_superuser or user.groups.filter(name=getattr(settings, 'QANDA_EDITORS_GROUP_NAME', 'Editors')).exists():
			reply.deleted = True
	        reply.save()
	return HttpResponseRedirect(reverse(question_page, args=(reply.answer.question.pk,)))


##############################################
#
# INDEX PAGES
#
##############################################

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
@login_required
def profile_page(request, user_id):
	context = {}
	qandaUser = get_object_or_404(QandaUser, pk=user_id)
	context['qandaUser'] = qandaUser
	return render_to_response("qanda/profile.html", context, context_instance=RequestContext(request))

@assert_qanda_user
def question_list(request, question_id, category):
	context = {}
	category = Category.objects.filter(slug=category)
	if category.exists():
		category = category[0]
	else:
		category = None

	if int(question_id) <= 0:
		try:
			question_id = Question.objects.latest('pk').pk
		except:
			pass

	if category:
		questions = Question.objects.filter(category=category, pk__lte=question_id, deleted=False).order_by('-postDate')[:NUM_OF_QUESTIONS_PER_PAGE]
	else:
		questions = Question.objects.filter(pk__lte=question_id, deleted=False).order_by('-postDate')[:NUM_OF_QUESTIONS_PER_PAGE]

	for question in questions:
		question.voteCount = QuestionRelatedUsers.objects.filter(relatedQuestion=question, upvote=True).count() - QuestionRelatedUsers.objects.filter(relatedQuestion=question, downvote=True).count()
	context['questions'] = questions
	context['view'] = 'question_list'

	if len(questions) > 0:
		if category:
			next_qset = Question.objects.filter(category=category, pk__gte=questions[0].pk+1, deleted=False).order_by('-postDate')[:1]
		else:
			next_qset = Question.objects.filter(pk__gte=questions[0].pk+1, deleted=False).order_by('-postDate')[:1]

		if next_qset.exists():
			if next_qset[0].pk > int(question_id):
				context['next'] = next_qset[0].pk

		if category:
			prev_qset = Question.objects.filter(category=category, pk__lte=questions[len(questions)-1].pk-1, deleted=False).order_by('-postDate')[:1]
		else:
			prev_qset = Question.objects.filter(pk__lte=questions[len(questions)-1].pk-1, deleted=False).order_by('-postDate')[:1]
		if prev_qset.exists():
			context['prev'] = prev_qset[0].pk

	context['categories'] = Category.objects.all()
	context['category'] = category

	return render_to_response("qanda/question_list.html", context, context_instance=RequestContext(request))

@assert_qanda_user
def user_starred_questions_list(request, user_id, question_id, category):
	context = {}
	qandaUser = get_object_or_404(QandaUser, pk=user_id)
	category = Category.objects.filter(slug=category)
	if category.exists():
		category = category[0]
	else:
		category = None

	if int(question_id) <= 0:
		try:
			question_id = Question.objects.latest('pk').pk
		except:
			pass

	if category:
		questions = Question.objects.filter(user_relation__relatedUser=qandaUser, user_relation__star=True, category=category, pk__lte=question_id, deleted=False).order_by('-postDate')[:NUM_OF_QUESTIONS_PER_PAGE]
	else:
		questions = Question.objects.filter(user_relation__relatedUser=qandaUser, user_relation__star=True, pk__lte=question_id, deleted=False).order_by('-postDate')[:NUM_OF_QUESTIONS_PER_PAGE]
	
	for question in questions:
		question.voteCount = QuestionRelatedUsers.objects.filter(relatedQuestion=question, upvote=True).count() - QuestionRelatedUsers.objects.filter(relatedQuestion=question, downvote=True).count()
	context['questions'] = questions
	context['view'] = 'user_starred_questions_list'

	if len(questions) > 0:
		if category:
			next_qset = Question.objects.filter(user_relation__relatedUser=qandaUser, user_relation__star=True, category=category, pk__gte=questions[0].pk+1, deleted=False).order_by('-postDate')[:1]
		else:
			next_qset = Question.objects.filter(user_relation__relatedUser=qandaUser, user_relation__star=True, pk__gte=questions[0].pk+1, deleted=False).order_by('-postDate')[:1]
		if next_qset.exists():
			if next_qset[0].pk > int(question_id):
				context['next'] = next_qset[0].pk

		if category:
			prev_qset = Question.objects.filter(user_relation__relatedUser=qandaUser, user_relation__star=True, category=category, pk__lte=questions[len(questions)-1].pk-1, deleted=False).order_by('-postDate')[:1]
		else:
			prev_qset = Question.objects.filter(user_relation__relatedUser=qandaUser, user_relation__star=True, pk__lte=questions[len(questions)-1].pk-1, deleted=False).order_by('-postDate')[:1]
		if prev_qset.exists():
			context['prev'] = prev_qset[0].pk

	context['categories'] = Category.objects.all()
	context['qandaUser'] = qandaUser
	context['category'] = category

	return render_to_response("qanda/question_list.html", context, context_instance=RequestContext(request))

@assert_qanda_user
def user_asked_questions_list(request, user_id, question_id, category):
	context = {}
	qandaUser = get_object_or_404(QandaUser, pk=user_id)
	category = Category.objects.filter(slug=category)
	if category.exists():
		category = category[0]
	else:
		category = None

	if int(question_id) <= 0:
		try:
			question_id = Question.objects.latest('pk').pk
		except:
			pass

	if category:
		questions = Question.objects.filter(author=qandaUser, category=category, pk__lte=question_id, deleted=False).order_by('-postDate')[:NUM_OF_QUESTIONS_PER_PAGE]
	else:
		questions = Question.objects.filter(author=qandaUser, pk__lte=question_id, deleted=False).order_by('-postDate')[:NUM_OF_QUESTIONS_PER_PAGE]
	
	for question in questions:
		question.voteCount = QuestionRelatedUsers.objects.filter(relatedQuestion=question, upvote=True).count() - QuestionRelatedUsers.objects.filter(relatedQuestion=question, downvote=True).count()
	context['questions'] = questions
	context['view'] = 'user_asked_questions_list'

	if len(questions) > 0:
		if category:
			next_qset = Question.objects.filter(author=qandaUser, category=category, pk__gte=questions[0].pk+1, deleted=False).order_by('-postDate')[:1]
		else:
			next_qset = Question.objects.filter(author=qandaUser, pk__gte=questions[0].pk+1, deleted=False).order_by('-postDate')[:1]
		if next_qset.exists():
			if next_qset[0].pk > int(question_id):
				context['next'] = next_qset[0].pk

		if category:
			prev_qset = Question.objects.filter(author=qandaUser, category=category, pk__lte=questions[len(questions)-1].pk-1, deleted=False).order_by('-postDate')[:1]
		else:
			prev_qset = Question.objects.filter(author=qandaUser, pk__lte=questions[len(questions)-1].pk-1, deleted=False).order_by('-postDate')[:1]
		if prev_qset.exists():
			context['prev'] = prev_qset[0].pk

	context['categories'] = Category.objects.all()
	context['qandaUser'] = qandaUser
	context['category'] = category

	return render_to_response("qanda/question_list.html", context, context_instance=RequestContext(request))

@assert_qanda_user
def user_answered_questions_list(request, user_id, question_id, category):
	context = {}
	qandaUser = get_object_or_404(QandaUser, pk=user_id)
	category = Category.objects.filter(slug=category)
	if category.exists():
		category = category[0]
	else:
		category = None

	if int(question_id) <= 0:
		try:
			question_id = Question.objects.latest('pk').pk
		except:
			pass

	if category:
		questions = Question.objects.filter(answers__author=qandaUser, category=category, pk__lte=question_id, deleted=False).order_by('-postDate')[:NUM_OF_QUESTIONS_PER_PAGE]
	else:
		questions = Question.objects.filter(answers__author=qandaUser, pk__lte=question_id, deleted=False).order_by('-postDate')[:NUM_OF_QUESTIONS_PER_PAGE]
	
	for question in questions:
		question.voteCount = QuestionRelatedUsers.objects.filter(relatedQuestion=question, upvote=True).count() - QuestionRelatedUsers.objects.filter(relatedQuestion=question, downvote=True).count()
	context['questions'] = questions
	context['view'] = 'user_answered_questions_list'

	if len(questions) > 0:
		if category:
			next_qset = Question.objects.filter(answers__author=qandaUser, category=category, pk__gte=questions[0].pk+1, deleted=False).order_by('-postDate')[:1]
		else:
			next_qset = Question.objects.filter(answers__author=qandaUser, pk__gte=questions[0].pk+1, deleted=False).order_by('-postDate')[:1]
		if next_qset.exists():
			if next_qset[0].pk > int(question_id):
				context['next'] = next_qset[0].pk

		if category:
			prev_qset = Question.objects.filter(answers__author=qandaUser, category=category, pk__lte=questions[len(questions)-1].pk-1, deleted=False).order_by('-postDate')[:1]
		else:
			prev_qset = Question.objects.filter(answers__author=qandaUser, pk__lte=questions[len(questions)-1].pk-1, deleted=False).order_by('-postDate')[:1]
		if prev_qset.exists():
			context['prev'] = prev_qset[0].pk

	context['categories'] = Category.objects.all()
	context['qandaUser'] = qandaUser
	context['category'] = category

	return render_to_response("qanda/question_list.html", context, context_instance=RequestContext(request))

@assert_qanda_user
def user_replied_questions_list(request, user_id, question_id, category):
	context = {}
	qandaUser = get_object_or_404(QandaUser, pk=user_id)
	category = Category.objects.filter(slug=category)
	if category.exists():
		category = category[0]
	else:
		category = None

	if int(question_id) <= 0:
		try:
			question_id = Question.objects.latest('pk').pk
		except:
			pass

	if category:
		questions = Question.objects.filter(answers__replies__author=qandaUser, category=category, pk__lte=question_id, deleted=False).order_by('-postDate')[:NUM_OF_QUESTIONS_PER_PAGE]
	else:
		questions = Question.objects.filter(answers__replies__author=qandaUser, pk__lte=question_id, deleted=False).order_by('-postDate')[:NUM_OF_QUESTIONS_PER_PAGE]
	
	for question in questions:
		question.voteCount = QuestionRelatedUsers.objects.filter(relatedQuestion=question, upvote=True).count() - QuestionRelatedUsers.objects.filter(relatedQuestion=question, downvote=True).count()
	context['questions'] = questions
	context['view'] = 'user_replied_questions_list'

	if len(questions) > 0:
		if category:
			next_qset = Question.objects.filter(answers__replies__author=qandaUser, category=category, pk__gte=questions[0].pk+1, deleted=False).order_by('-postDate')[:1]
		else:
			next_qset = Question.objects.filter(answers__replies__author=qandaUser, pk__gte=questions[0].pk+1, deleted=False).order_by('-postDate')[:1]
		if next_qset.exists():
			if next_qset[0].pk > int(question_id):
				context['next'] = next_qset[0].pk

		if category:
			prev_qset = Question.objects.filter(answers__replies__author=qandaUser, category=category, pk__lte=questions[len(questions)-1].pk-1, deleted=False).order_by('-postDate')[:1]
		else:
			prev_qset = Question.objects.filter(answers__replies__author=qandaUser, pk__lte=questions[len(questions)-1].pk-1, deleted=False).order_by('-postDate')[:1]
		if prev_qset.exists():
			context['prev'] = prev_qset[0].pk

	context['categories'] = Category.objects.all()
	context['qandaUser'] = qandaUser
	context['category'] = category

	return render_to_response("qanda/question_list.html", context, context_instance=RequestContext(request))

@assert_qanda_user
def category_list(request, page):
	context = {}
	page = int(page)
	
	categories = Category.objects.order_by('name')[page*(NUM_OF_TAGS_PER_PAGE):(page+1)*NUM_OF_TAGS_PER_PAGE]
	for category in categories:
		category.count = Question.objects.filter(category=category).count()

	context['categories'] = categories
	context['view'] = 'category_list'

	next_qset = Category.objects.order_by('name')[(page+1)*NUM_OF_TAGS_PER_PAGE:(page+2)*NUM_OF_TAGS_PER_PAGE]
	if next_qset.exists():
		context['next'] = page+1

	if page >= 1:
		prev_qset = Category.objects.order_by('name')[(page-1)*NUM_OF_TAGS_PER_PAGE:page*NUM_OF_TAGS_PER_PAGE]
		if prev_qset.exists():
			context['prev'] = page-1

	context['current_page_number'] = page
	context['category_form'] = CategoryForm()

	return render_to_response("qanda/category_list.html", context, context_instance=RequestContext(request))


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

	context['current_page_number'] = page

	return render_to_response("qanda/tag_list.html", context, context_instance=RequestContext(request))

@assert_qanda_user
def tag_page(request, tag, page):
	context = {}
	page = int(page)
	questions = Question.objects.filter(tags__name__in=[tag], deleted=False).order_by('-postDate')[page*(NUM_OF_QUESTIONS_PER_PAGE):(page+1)*NUM_OF_QUESTIONS_PER_PAGE]
	for question in questions:
		question.voteCount = QuestionRelatedUsers.objects.filter(relatedQuestion=question, upvote=True).count
	context['questions'] = questions
	context['tag'] = tag
	context['view'] = 'tag_page'

	next_qset = Question.objects.filter(tags__name__in=[tag], deleted=False).order_by('-postDate')[(page+1)*NUM_OF_QUESTIONS_PER_PAGE:(page+2)*NUM_OF_QUESTIONS_PER_PAGE]
	if next_qset.exists():
		context['next'] = page+1

	if page >= 1:
		prev_qset = Question.objects.filter(tags__name__in=[tag], deleted=False).order_by('-postDate')[(page-1)*NUM_OF_QUESTIONS_PER_PAGE:page*NUM_OF_QUESTIONS_PER_PAGE]
		if prev_qset.exists():
			context['prev'] = page-1

	context['categories'] = Category.objects.all()
	context['current_page_number'] = page

	return render_to_response("qanda/tag_page.html", context, context_instance=RequestContext(request))

@assert_qanda_user
def categorized_tag_page(request, category, tag, page):
	context = {}
	page = int(page)
	category_id = get_object_or_404(Category, slug=category)
	questions = Question.objects.filter(category=category_id, tags__name__in=[tag], deleted=False).order_by('-postDate')[page*(NUM_OF_QUESTIONS_PER_PAGE):(page+1)*NUM_OF_QUESTIONS_PER_PAGE]
	for question in questions:
		question.voteCount = QuestionRelatedUsers.objects.filter(relatedQuestion=question, upvote=True).count
	context['questions'] = questions
	context['tag'] = tag
	context['view'] = 'tag_page'

	next_qset = Question.objects.filter(category=category_id, tags__name__in=[tag], deleted=False).order_by('-postDate')[(page+1)*NUM_OF_QUESTIONS_PER_PAGE:(page+2)*NUM_OF_QUESTIONS_PER_PAGE]
	if next_qset.exists():
		context['next'] = page+1

	if page >= 1:
		prev_qset = Question.objects.filter(category=category_id, tags__name__in=[tag], deleted=False).order_by('-postDate')[(page-1)*NUM_OF_QUESTIONS_PER_PAGE:page*NUM_OF_QUESTIONS_PER_PAGE]
		if prev_qset.exists():
			context['prev'] = page-1

	context['categories'] = Category.objects.all()
	context['current_page_number'] = page

	return render_to_response("qanda/tag_page.html", context, context_instance=RequestContext(request))

@assert_qanda_user
def most_recent_question(request):
	try:
		latest_question = Question.objects.filter(deleted=False).latest('postDate')
		return HttpResponseRedirect(reverse(question_page, args=(latest_question.pk,)))
	except:
		return HttpResponseRedirect(reverse(new_question_page, args=()))

@assert_qanda_user
@login_required
def edit_question_page(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	if not question.deleted or not question.closed:
		if not question.author.djangoUser == get_user(request):
			raise Http404
		context = {}
		context['type'] = 'new_question'

		if request.method == 'POST':
			if request.POST['type'] == 'new_question':
				question_form = QuestionForm(request.POST)
				context['question_form'] = question_form
				if question_form.is_valid():
					qandaUser = get_user(request).QandaUser
					edited_data = question_form.cleaned_data
					question.title = edited_data['title']
					if edited_data['category']:
						question.category = edited_data['category']
					question.text = edited_data['text']
					question.save()
					question.tags.clear()
					for tag in edited_data['tags']:
						question.tags.add(tag)
					return HttpResponseRedirect(reverse(question_page, args=(question.pk,)))
		else:
			context['question_form'] = QuestionForm(instance=question)

		context['view'] = 'new_question_page'
		context['debug'] = ''

		return render_to_response("qanda/edit_question.html", context, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect(reverse(question_page, args=(question.pk,)))

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

	return render_to_response("qanda/new_question.html", context, context_instance=RequestContext(request))

def question_page(request, question_id):
	context = {}
	if not Question.objects.exists():
		context = {}
		context['type'] = 'new_question'
		context['question_form'] = QuestionForm()
		return HttpResponseRedirect(reverse(new_question_page, args=()))
	question = get_object_or_404(Question, pk=question_id)
	if not question.deleted:
		question.numOfVotes = QuestionRelatedUsers.objects.filter(relatedQuestion=question, upvote=True).count() - QuestionRelatedUsers.objects.filter(relatedQuestion=question, downvote=True).count()
		user = get_user(request)
		if user.is_authenticated():
			all_relations = QuestionRelatedUsers.objects.filter(relatedQuestion=question, relatedUser__djangoUser=get_user(request))
			if all_relations.count() > 0: 
				existingRelation = all_relations[0]
				question.relations = all_relations[0]
				existingRelation.seen = True
				existingRelation.save()
			else:
				newRelation = QuestionRelatedUsers.objects.create(relatedUser=user.QandaUser, 
                                                                relatedQuestion=question,
                                                                upvote=False,
                                                                downvote=False,
                                                                useful=False,
                                                                notUseful=False,
                                                                star=False,
                                                                flag=False,
                                                                seen=True)
				newRelation.save()
				
		answers = question.answers.filter(deleted=False)
		for answer in answers:
			answer.numOfVotes = AnswerRelatedUsers.objects.filter(relatedAnswer=answer, upvote=True).count() - AnswerRelatedUsers.objects.filter(relatedAnswer=answer, downvote=True).count()
		answers = sorted(answers, key=lambda answer: -answer.numOfVotes)

		if user.is_authenticated():
			relations = question.user_relation.filter(relatedUser=user.QandaUser)
			if relations.exists():
				relations = relations[0]
				question.relations = relations
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
			context['question_close_form'] = QuestionCloseForm()

		context['question'] = question
		context['answers'] = answers
		context['is_editor'] = user.groups.filter(name=getattr(settings, 'QANDA_EDITORS_GROUP_NAME', 'Editors'))
		context['debug'] = ''

		try:
			if question == Question.objects.filter(deleted=False).latest('pk'):
				context['view'] = 'last_question_page'
			else:
				context['view'] = 'question_page'
		except:
			context['view'] = 'question_page'

		return render_to_response('qanda/question.html', context, context_instance=RequestContext(request))
	else:
		raise Http404


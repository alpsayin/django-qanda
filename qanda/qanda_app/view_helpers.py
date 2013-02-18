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
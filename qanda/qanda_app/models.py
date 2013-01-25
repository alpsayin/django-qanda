from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class QandaUserManager(models.Manager):
	"""
		Manager object for QandaUser type
	"""
	def create_user(self, django_user):
		newQandaUser=self.create(djangoUser=django_user, deleted=False)
		return newQandaUser
	def star(self, qandaUser1, qandaUser2):
		if qandaUser1 is not qandaUser2:
			existingRelations = UserRelations.objects.filter(relater=qandaUser1, related=qandaUser2)
			if existingRelations.count() == 1:
				existingRelation = existingRelations[0]
				existingRelation.star = True
				existingRelation.save()
			elif existingRelations.count() == 0:
				newRelation = UserRelations.objects.create(relater=qandaUser1, related=qandaUser2, star=False, flag=False)
				newRelation.save()
			else:
				print 'SHOULDNT HAPPEN!!!'
	def unstar(self, qandaUser1, qandaUser2):
		if qandaUser1 is not qandaUser2:
			existingRelations = UserRelations.objects.filter(relater=qandaUser1, related=qandaUser2)
			if existingRelations.count() == 1:
				existingRelation = existingRelations[0]
				existingRelation.star = False
				existingRelation.save()
			elif existingRelations.count() == 0:
				newRelation = UserRelations.objects.create(relater=qandaUser1, related=qandaUser2, star=False, flag=False)
				newRelation.save()
			else:
				print 'SHOULDNT HAPPEN!!!'
	def flag(self, qandaUser1, qandaUser2):
		if qandaUser1 is not qandaUser2:
			existingRelations = UserRelations.objects.filter(relater=qandaUser1, related=qandaUser2)
			if existingRelations.count() == 1:
				existingRelation = existingRelations[0]
				existingRelation.flag = True
				existingRelation.save()
			elif existingRelations.count() == 0:
				newRelation = UserRelations.objects.create(relater=qandaUser1, related=qandaUser2, star=False, flag=True)
				newRelation.save()
			else:
				print 'SHOULDNT HAPPEN!!!'
	def unflag(self, qandaUser1, qandaUser2):
		if qandaUser1 is not qandaUser2:
			existingRelations = UserRelations.objects.filter(relater=qandaUser1, related=qandaUser2)
			if existingRelations.count() == 1:
				existingRelation = existingRelations[0]
				existingRelation.flag = False
				existingRelation.save()
			elif existingRelations.count() == 0:
				newRelation = UserRelations.objects.create(relater=qandaUser1, related=qandaUser2, star=False, flag=False)
				newRelation.save()
			else:
				print 'SHOULDNT HAPPEN!!!'

class QandaUser(models.Model):
	"""
		User information regarding the Qanda Application
	"""
	objects = QandaUserManager()
	djangoUser = models.OneToOneField(User, related_name='QandaUser')
	# answers - foreign key of Answer
	# questions - foreign key of Question
	# replies - foreign key of Reply
	deleted = models.BooleanField()
	relatedUsers = models.ManyToManyField("self", symmetrical=False, through='UserRelations', related_name='relaterUsers')
	tags = TaggableManager()
	class Meta:
		verbose_name = 'Qanda User'
	def __unicode__(self):
		return u'%s %s' % (self.djangoUser.first_name, self.djangoUser.last_name)

class QuestionManager(models.Manager):
	"""
		Manager object for Question type
	"""
	def create_question(self, question_title, qanda_user, question_text):
		newQuestion = self.create(	title=question_title,
									text=question_text,
									author=qanda_user,
									viewCount=0,
									closeMessage='',
									deleted=False,
									closed=False)
		return newQuestion
	def star(self, qandaUser, question):
		existingRelations = QuestionRelatedUsers.objects.filter(relatedUser=qandaUser, relatedQuestion=question)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.star = True
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = QuestionRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedQuestion=question,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=True,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def unstar(self, qandaUser, question):
		existingRelations = QuestionRelatedUsers.objects.filter(relatedUser=qandaUser, relatedQuestion=question)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.star = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = QuestionRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedQuestion=question,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def flag(self, qandaUser, question):
		existingRelations = QuestionRelatedUsers.objects.filter(relatedUser=qandaUser, relatedQuestion=question)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.flag = True
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = QuestionRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedQuestion=question,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=True)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def unflag(self, qandaUser, question):
		existingRelations = QuestionRelatedUsers.objects.filter(relatedUser=qandaUser, relatedQuestion=question)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.flag = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = QuestionRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedQuestion=question,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def upvote(self, qandaUser, question):
		existingRelations = QuestionRelatedUsers.objects.filter(relatedUser=qandaUser, relatedQuestion=question)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.upvote = True
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = QuestionRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedQuestion=question,
																upvote=True,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'

	def unupvote(self, qandaUser, question):
		existingRelations = QuestionRelatedUsers.objects.filter(relatedUser=qandaUser, relatedQuestion=question)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.upvote = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = QuestionRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedQuestion=question,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def downvote(self, qandaUser, question):
		existingRelations = QuestionRelatedUsers.objects.filter(relatedUser=qandaUser, relatedQuestion=question)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.downvote = True
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = QuestionRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedQuestion=question,
																upvote=False,
																downvote=True,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def undownvote(self, qandaUser, question):
		existingRelations = QuestionRelatedUsers.objects.filter(relatedUser=qandaUser, relatedQuestion=question)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.downvote = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = QuestionRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedQuestion=question,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def useful(self, qandaUser, question):
		existingRelations = QuestionRelatedUsers.objects.filter(relatedUser=qandaUser, relatedQuestion=question)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.useful = True
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = QuestionRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedQuestion=question,
																upvote=False,
																downvote=False,
																useful=True,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def unuseful(self, qandaUser, question):
		existingRelations = QuestionRelatedUsers.objects.filter(relatedUser=qandaUser, relatedQuestion=question)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.useful = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = QuestionRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedQuestion=question,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def notUseful(self, qandaUser, question):
		existingRelations = QuestionRelatedUsers.objects.filter(relatedUser=qandaUser, relatedQuestion=question)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.notUseful = True
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = QuestionRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedQuestion=question,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=True,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def unnotUseful(self, qandaUser, question):
		existingRelations = QuestionRelatedUsers.objects.filter(relatedUser=qandaUser, relatedQuestion=question)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.notUseful = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = QuestionRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedQuestion=question,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'

class Question(models.Model):
	"""
		Model to hold questions
	"""
	objects = QuestionManager()
	title = models.CharField(max_length=255)
	text = models.TextField(blank=True);
	author = models.ForeignKey(QandaUser, related_name='questions')
	viewCount = models.IntegerField()
	postDate = models.DateTimeField(auto_now_add=True)
	editDate = models.DateTimeField(auto_now=True)
	closeMessage = models.TextField(blank=True)
	closeDate = models.DateTimeField(auto_now=True)
	deleted = models.BooleanField()
	closed = models.BooleanField()
	tags = TaggableManager()
	#answers - foreign key of Answer
	relatedUsers = models.ManyToManyField(QandaUser, through='QuestionRelatedUsers', related_name='related_questions')
	class Meta:
		verbose_name = 'Qanda Question'
	def __unicode__(self):
		return u'%d %s' % (self.pk, self.title)

class AnswerManager(models.Manager):
	"""
		Manager object for Answer type
	"""
	def create_answer(self, question_id, qanda_user, answer_text):
		newAnswer = self.create(text=answer_text,
								question=question_id,
								author=qanda_user,
								deleted=False
								)
		return newAnswer
	def star(self, qandaUser, answer):
		existingRelations = AnswerRelatedUsers.objects.filter(relatedUser=qandaUser, relatedAnswer=answer)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.star = True
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = AnswerRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedAnswer=answer,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=True,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def unstar(self, qandaUser, answer):
		existingRelations = AnswerRelatedUsers.objects.filter(relatedUser=qandaUser, relatedAnswer=answer)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.star = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = AnswerRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedAnswer=answer,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def flag(self, qandaUser, answer):
		existingRelations = AnswerRelatedUsers.objects.filter(relatedUser=qandaUser, relatedAnswer=answer)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.flag = True
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = AnswerRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedAnswer=answer,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=True)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def unflag(self, qandaUser, answer):
		existingRelations = AnswerRelatedUsers.objects.filter(relatedUser=qandaUser, relatedAnswer=answer)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.flag = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = AnswerRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedAnswer=answer,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def upvote(self, qandaUser, answer):
		existingRelations = AnswerRelatedUsers.objects.filter(relatedUser=qandaUser, relatedAnswer=answer)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.upvote = True
			existingRelation.downvote = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = AnswerRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedAnswer=answer,
																upvote=True,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'

	def unupvote(self, qandaUser, answer):
		existingRelations = AnswerRelatedUsers.objects.filter(relatedUser=qandaUser, relatedAnswer=answer)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.upvote = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = AnswerRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedAnswer=answer,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def downvote(self, qandaUser, answer):
		existingRelations = AnswerRelatedUsers.objects.filter(relatedUser=qandaUser, relatedAnswer=answer)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.downvote = True
			existingRelation.upvote = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = AnswerRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedAnswer=answer,
																upvote=False,
																downvote=True,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def undownvote(self, qandaUser, answer):
		existingRelations = AnswerRelatedUsers.objects.filter(relatedUser=qandaUser, relatedAnswer=answer)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.downvote = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = AnswerRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedAnswer=answer,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def useful(self, qandaUser, answer):
		existingRelations = AnswerRelatedUsers.objects.filter(relatedUser=qandaUser, relatedAnswer=answer)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.useful = True
			existingRelation.notUseful = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = AnswerRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedAnswer=answer,
																upvote=False,
																downvote=False,
																useful=True,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def unuseful(self, qandaUser, answer):
		existingRelations = AnswerRelatedUsers.objects.filter(relatedUser=qandaUser, relatedAnswer=answer)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.useful = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = AnswerRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedAnswer=answer,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def notUseful(self, qandaUser, answer):
		existingRelations = AnswerRelatedUsers.objects.filter(relatedUser=qandaUser, relatedAnswer=answer)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.notUseful = True
			existingRelation.useful = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = AnswerRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedAnswer=answer,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=True,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'
	def unnotUseful(self, qandaUser, answer):
		existingRelations = AnswerRelatedUsers.objects.filter(relatedUser=qandaUser, relatedAnswer=answer)
		if existingRelations.count() == 1:
			existingRelation = existingRelations[0]
			existingRelation.notUseful = False
			existingRelation.save()
		elif existingRelations.count() == 0:
			newRelation = AnswerRelatedUsers.objects.create(relatedUser=qandaUser, 
																relatedAnswer=answer,
																upvote=False,
																downvote=False,
																useful=False,
																notUseful=False,
																star=False,
																flag=False)
			newRelation.save()
		else:
			print 'SHOULDNT HAPPEN!'

class Answer(models.Model):
	"""
		Model to hold answers to questions
	"""
	objects = AnswerManager()
	text = models.TextField()
	question = models.ForeignKey(Question, related_name='answers')
	author = models.ForeignKey(QandaUser, related_name='answers')
	# replies - foreign key of Reply
	relatedUsers = models.ManyToManyField(QandaUser, through='AnswerRelatedUsers', related_name='related_answers')
	postDate = models.DateTimeField(auto_now_add=True)
	editDate = models.DateTimeField(auto_now=True)
	deleted = models.BooleanField()
	class Meta:
		verbose_name = 'Qanda Answer'
	def __unicode__(self):
		return u'%d by %s' % (self.pk, self.author.djangoUser)

class ReplyManager(models.Manager):
	"""
		Manager object for Reply Type
	"""
	def create_reply(self, answer_id, qanda_user, reply_text):
		newReply = self.create(text = reply_text,
								author = qanda_user,
								answer = answer_id,
								deleted = False)
		return newReply

class Reply(models.Model):
	"""
		Model to hold replies to answers
	"""
	objects = ReplyManager()
	text = models.TextField()
	author = models.ForeignKey(QandaUser, related_name='replies')
	answer = models.ForeignKey(Answer, null=True, related_name='replies')
	postDate = models.DateTimeField(auto_now_add=True)
	editDate = models.DateTimeField(auto_now=True)
	deleted = models.BooleanField()
	class Meta:
		verbose_name = 'Qanda Reply'
	def __unicode__(self):
		return u'%d by %s' % (self.pk, self.author.djangoUser)


class UserRelations(models.Model):
	"""
		Relationship table to hold user starring relations
	"""
	relater = models.ForeignKey(QandaUser, related_name='relaterRelation')
	related = models.ForeignKey(QandaUser, related_name='relatedRelation')
	star = models.BooleanField()
	flag = models.BooleanField()
	class Meta:
		verbose_name = 'Qanda User Relationship'
	def __unicode__(self):
		return u'%s -> %s : [S:%d, F:%d]' % (self.relater.djangoUser.username, self.related.djangoUser.username, self.star, self.flag)


class QuestionRelatedUsers(models.Model):
	"""
		Relationship table to hold the various relations of users with questions such as:
			up-vote
			down-vote
			useful
			not-useful
			star
			flag
	"""
	relatedUser = models.ForeignKey(QandaUser, related_name='question_relation')
	relatedQuestion = models.ForeignKey(Question, related_name='user_relation')
	upvote = models.BooleanField()
	downvote = models.BooleanField()
	useful = models.BooleanField()
	notUseful = models.BooleanField()
	star = models.BooleanField()
	flag = models.BooleanField()
	class Meta:
		verbose_name = 'Qanda Question/User Relationship'

class AnswerRelatedUsers(models.Model):
	"""
		Relationship table to hold the various relations of users with answers such as:
			up-vote
			down-vote
			useful
			not-useful
			star
			flag
	"""
	relatedUser = models.ForeignKey(QandaUser, related_name='answer_relation')
	relatedAnswer = models.ForeignKey(Answer, related_name='user_relation')
	upvote = models.BooleanField()
	downvote = models.BooleanField()
	useful = models.BooleanField()
	notUseful = models.BooleanField()
	star = models.BooleanField()
	flag = models.BooleanField()
	class Meta:
		verbose_name = 'Qanda Answer/User Relationship'

class QandaUserStats(models.Model):
	"""
		THIS TABLE IS FOR FUTURE USE
		Statistics table to hold various statistics about a QandaUser, such as the number of:
			profileViews
			Questions
			Answers
			Replies
			Tags
			Starred Users
			His Starred Users
			Upvoted Questions
			His Upvoted Questions
			Downvoted Questions
			His Downvoted Questions
			Useful Questions
			His Useful Questions
			Not Useful Questions
			His Not Useful Questions
			Flagged Questions
			His Flagged Questions
			Starred Questions
			His Starred Questions
			Upvoted Answers
			His Upvoted Answers
			Downvoted Answers
			His Downvoted Answers
			Useful Answers
			His Useful Answers
			Not Useful Answers
			His Not Useful Answers
			Flagged Answers
			His Flagged Answers
			Starred Answers
			His Starred Answers
	"""
	qandaUser = models.OneToOneField(QandaUser)
	profileViews = models.IntegerField()
	questions = models.IntegerField()
	answers = models.IntegerField()
	replies = models.IntegerField()
	tags = models.IntegerField()
	starredUsers = models.IntegerField()
	hisStarredUsers = models.IntegerField()
	upvotedQuestions = models.IntegerField()
	hisUpvotedQuestions = models.IntegerField()
	downvotedQuestions = models.IntegerField()
	hisDownvotedQuestions = models.IntegerField()
	usefulQuestions = models.IntegerField()
	hisUsefulQuestions = models.IntegerField()
	notUsefulQuestions = models.IntegerField()
	hisNotUsefulQuestions = models.IntegerField()
	flaggedQuestions = models.IntegerField()
	hisFlaggedQuestions = models.IntegerField()
	starredQuestions = models.IntegerField()
	hisStarredQuestions = models.IntegerField()
	upvotedAnswers = models.IntegerField()
	hisUpvotedAnswers = models.IntegerField()
	downvotedAnswers = models.IntegerField()
	hisDownvotedAnswers = models.IntegerField()
	usefulAnswers = models.IntegerField()
	hisUsefulAnswers = models.IntegerField()
	notUsefulAnswers = models.IntegerField()
	hisNotUsefulAnswers = models.IntegerField()
	flaggedAnswers = models.IntegerField()
	hisFlaggedAnswers = models.IntegerField()
	starredAnswers = models.IntegerField()
	hisStarredAnswers = models.IntegerField()
	class Meta:
		verbose_name = 'Qanda User Statistic'
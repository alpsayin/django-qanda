from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.

class QandaUser(models.Model):
	"""
		User information regarding the Qanda Application
	"""
	djangoUser = models.OneToOneField(User, related_name='QandaUser')
	# answers - foreign key of Answer
	# questions - foreign key of Question
	# replies - foreign key of Reply
	deleted = models.BooleanField()
	starred = models.ManyToManyField("self", null=True, symmetrical=False, through='UserStars', related_name='starred_by')
	tags = TaggableManager()
	class Meta:
		verbose_name = 'Qanda User'
	def __unicode__(self):
		return u'%s %s' % (self.djangoUser.first_name, self.djangoUser.last_name)


class Question(models.Model):
	"""
		Model to hold questions
	"""
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

class Answer(models.Model):
	"""
		Model to hold answers to questions
	"""
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

class Reply(models.Model):
	"""
		Model to hold replies to answers
	"""
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


class UserStars(models.Model):
	"""
		Relationship table to hold user starring relations
	"""
	starrer = models.ForeignKey(QandaUser, related_name='starrer_relation')
	starred = models.ForeignKey(QandaUser, related_name='starred_relation')
	timestamp = models.DateTimeField(auto_now=True)
	class Meta:
		verbose_name = 'Qanda Star Relationship'

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
	relatedUser = models.ForeignKey(QandaUser)
	relatedQuestion = models.ForeignKey(Question)
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
	relatedUser = models.ForeignKey(QandaUser)
	relatedQuestion = models.ForeignKey(Answer)
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
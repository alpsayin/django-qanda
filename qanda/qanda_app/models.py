from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.db.models import signals
from django_notify import models as notify_models
from django_notify.models import Subscription, Settings, NotificationType, Notification
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

# Create your models here.
class QandaUserManager(models.Manager):
    """
        Manager object for QandaUser type
    """
    def create_user(self, django_user):
        newQandaUser=self.create(djangoUser=django_user, deleted=False)
        newQandaUserStat=QandaUserStats.create(qandaUser=newQandaUser)
        return newQandaUser
    def star(self, qandaUser1, qandaUser2):
        if qandaUser1 is not qandaUser2:
            existingRelations = UserRelations.objects.filter(relater=qandaUser1, related=qandaUser2)
            if existingRelations.count() == 1:
                existingRelation = existingRelations[0]
                existingRelation.star = True
                existingRelation.save()
            elif existingRelations.exists():
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
            elif existingRelations.exists():
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
            elif existingRelations.exists():
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
            elif existingRelations.exists():
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
    tags = TaggableManager(blank=True)
    class Meta:
        verbose_name = 'Qanda User'
    def __unicode__(self):
        return u'%s %s' % (self.djangoUser.first_name, self.djangoUser.last_name)

class QuestionManager(models.Manager):
    """
        Manager object for Question type
    """
    def create_question(self, qanda_user, question_title, question_text):
        newQuestion = self.create(    title=question_title,
                                    text=question_text,
                                    author=qanda_user,
                                    viewCount=0,
                                    closeMessage='',
                                    deleted=False,
                                    closed=False)
        return newQuestion

    def increment_view_count(self, question):
        question.viewCount = question.viewCount + 1
        question.save()
        return question.viewCount

    def edit_question(self, question, new_title, new_text, tags):
        question.title = new_title
        question.text = new_text
        question.tags = tags
        question.save()

    def subscribe_to_question(self, question, qandaUser, subscribe):
        if subscribe:
            [settings, created] = Settings.objects.get_or_create(user=qandaUser.djangoUser,)
            if created:
                settings.save()
            [subscription, created] = QuestionSubscription.objects.get_or_create(settings=settings,
                                                                                 question=question,
                                                                                 object_id=str(question.pk),
                                                                                 notification_type=NotificationType.objects.get_or_create(key="new_answer",
                                                                                                                                          content_type=ContentType.objects.get_for_model(Answer))[0])
            if created:
                subscription.send_emails = True
                subscription.save()
                pass

        else:
            subscription = QuestionSubscription.objects.filter(settings__user=qandaUser.djangoUser,
                                                            question=question,
                                                            object_id=str(question.pk),
                                                            )
            notifications = Notification.objects.filter(subscription=subscription).delete()
            subscription.delete()

    def set_relations(self, qandaUser, question, relations):
        existingRelations = QuestionRelatedUsers.objects.filter(relatedUser=qandaUser, relatedQuestion=question)
        if not existingRelations.exists():
            existingRelation = QuestionRelatedUsers.objects.create(relatedUser=qandaUser, 
                                                                relatedQuestion=question,
                                                                upvote=False,
                                                                downvote=False,
                                                                useful=False,
                                                                notUseful=False,
                                                                star=False,
                                                                flag=False)
        elif existingRelations.count() == 1:
            existingRelation = existingRelations[0]
        elif existingRelations.count() > 1:
            print 'SHOULDNT HAPPEN'
        else:
            print 'ALSO SHOULDNT HAPPEN'

        for counter,relation in enumerate(relations):
            value = relations[relation]
            if relation == 'star':
                existingRelation.star = value

            elif relation == 'flag':
                existingRelation.flag = value

            elif relation == 'upvote':
                existingRelation.upvote = value
                if value:
                    existingRelation.downvote = False

            elif relation == 'downvote':
                existingRelation.downvote = value
                if value:
                    existingRelation.upvote = False

            elif relation == 'useful':
                existingRelation.useful = value
                if value:
                    existingRelation.notUseful = False

            elif relation == 'notUseful':
                existingRelation.notUseful = value
                if value:
                    existingRelation.useful = False

        existingRelation.save()

class Question(models.Model):
    """
        Model to hold questions
    """
    objects = QuestionManager()
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True);
    author = models.ForeignKey(QandaUser, related_name='questions')
    viewCount = models.IntegerField(default=0)
    postDate = models.DateTimeField(auto_now_add=True)
    editDate = models.DateTimeField(auto_now=True)
    closeMessage = models.TextField(blank=True)
    closeDate = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField()
    closed = models.BooleanField()
    tags = TaggableManager(blank=True)
    category = models.ForeignKey('Category', null=True)
    #answers - foreign key of Answer
    relatedUsers = models.ManyToManyField(QandaUser, through='QuestionRelatedUsers', related_name='related_questions')
    class Meta:
        verbose_name = 'Qanda Question'

    def get_absolute_url(self):
        return reverse('qanda_app.views.question_page', args=(self.pk,))

    def __unicode__(self):
        return u'%d %s' % (self.pk, self.title)



class AnswerManager(models.Manager):
    """
        Manager object for Answer type
    """
    def create_answer(self, qanda_user, question_id, answer_text):
        newAnswer = self.create(text=answer_text,
                                question=question_id,
                                author=qanda_user,
                                deleted=False
                                )
        return newAnswer

    def edit_answer(self, answer, new_text):
        answer.text = new_text
        answer.save()

    def subscribe_to_answer(self, answer, qandaUser, subscribe):
        if subscribe:
            [settings, created] = Settings.objects.get_or_create(user=qandaUser.djangoUser,)
            if created:
                settings.save()
            [subscription, created] = AnswerSubscription.objects.get_or_create(settings=settings,
                                                                                 answer=answer,
                                                                                 object_id=str(answer.pk),
                                                                                 notification_type=NotificationType.objects.get_or_create(key="new_reply",
                                                                                                                                          content_type=ContentType.objects.get_for_model(Reply))[0])
            if created:
                subscription.send_emails = True
                subscription.save()
                pass

        else:
            subscription = AnswerSubscription.objects.filter(settings__user=qandaUser.djangoUser,
                                                            answer=answer,
                                                            object_id=str(answer.pk),
                                                            )
            notifications = Notification.objects.filter(subscription=subscription).delete()
            subscription.delete()


    def set_relations(self, qandaUser, answer, relations):
        existingRelations = AnswerRelatedUsers.objects.filter(relatedUser=qandaUser, relatedAnswer=answer)
        if not existingRelations.exists():
            existingRelation = AnswerRelatedUsers.objects.create(relatedUser=qandaUser, 
                                                                relatedAnswer=answer,
                                                                upvote=False,
                                                                downvote=False,
                                                                useful=False,
                                                                notUseful=False,
                                                                star=False,
                                                                flag=False)
        elif existingRelations.count() == 1:
            existingRelation = existingRelations[0]
        elif existingRelations.count() > 1:
            print 'SHOULDNT HAPPEN'
        else:
            print 'ALSO SHOULDNT HAPPEN'

        for counter,relation in enumerate(relations):
            value = relations[relation]
            if relation == 'star':
                existingRelation.star = value

            elif relation == 'flag':
                existingRelation.flag = value

            elif relation == 'upvote':
                existingRelation.upvote = value
                if value:
                    existingRelation.downvote = False

            elif relation == 'downvote':
                existingRelation.downvote = value
                if value:
                    existingRelation.upvote = False

            elif relation == 'useful':
                existingRelation.useful = value
                if value:
                    existingRelation.notUseful = False

            elif relation == 'notUseful':
                existingRelation.notUseful = value
                if value:
                    existingRelation.useful = False

        existingRelation.save()

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

    def get_absolute_url(self):
        return self.question.get_absolute_url()

    def __unicode__(self):
        return u'%d by %s' % (self.pk, self.author.djangoUser)

class ReplyManager(models.Manager):
    """
        Manager object for Reply Type
    """
    def create_reply(self, qanda_user, answer_id, reply_text):
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
        verbose_name_plural = 'Qanda Replies'
    def __unicode__(self):
        return u'%d by %s' % (self.pk, self.author.djangoUser)

class Category(models.Model):
    """
        A simple model to hold Question categories such as different sectors
    """
    category = models.CharField(max_length=255, unique=True)
    class Meta:
        verbose_name = "Qanda Category"
        verbose_name_plural = "Qanda Categories"
    def __unicode__(self):
        return u'%s' % (self.category)

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

from decorators import save_object_after
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
    qandaUser = models.OneToOneField(QandaUser, related_name='statistics')
    profileViews = models.IntegerField(default=0)
    tags = models.IntegerField(default=0)
    
    questions = models.IntegerField(default=0)
    @save_object_after
    def get_questions(self):
        self.questions = self.qandaUser.questions.count()
        return self.questions
    
    answers = models.IntegerField(default=0)
    @save_object_after
    def get_answers(self):
        self.answers = self.qandaUser.answers.count()
        return self.answers

    replies = models.IntegerField(default=0)
    @save_object_after
    def get_replies(self):
        self.replies = self.qandaUser.replies.count()
        return self.replies

    starredUsers = models.IntegerField(default=0)
    @save_object_after
    def get_user_stars_taken(self):
        self.starredUsers = UserRelations.objects.filter(related=self.qandaUser, star=True).count()
        return self.starredUsers

    hisStarredUsers = models.IntegerField(default=0)
    @save_object_after
    def get_user_stars_given(self):
        self.hisStarredUsers = UserRelations.objects.filter(relater=self.qandaUser, star=True).count()
        return self.hisStarredUsers

    flaggedUsers = models.IntegerField(default=0)
    @save_object_after
    def get_user_flags_taken(self):
        self.flaggedUsers = UserRelations.objects.filter(related=self.qandaUser, flag=True).count()
        return self.flaggedUsers

    hisFlaggedUsers = models.IntegerField(default=0)
    @save_object_after
    def get_user_flags_given(self):
        self.hisFlaggedUsers = UserRelations.objects.filter(relater=self.qandaUser, flag=True).count()
        return self.hisFlaggedUsers

    upvotedQuestions = models.IntegerField(default=0)
    @save_object_after
    def get_questions_upvotes_given(self):
        self.upvotedQuestions = QuestionRelatedUsers.objects.filter(relatedUser=self.qandaUser, upvote=True).count()
        return self.upvotedQuestions

    hisUpvotedQuestions = models.IntegerField(default=0)
    @save_object_after
    def get_question_upvotes_taken(self):
        self.hisUpvotedQuestions = QuestionRelatedUsers.objects.filter(relatedQuestion__author=self.qandaUser, upvote=True).count()
        return self.hisUpvotedQuestions

    downvotedQuestions = models.IntegerField(default=0)
    @save_object_after
    def get_question_downvotes_given(self):
        self.downvotedQuestions = QuestionRelatedUsers.objects.filter(relatedUser=self.qandaUser, downvote=True).count()
        return self.downvotedQuestions

    hisDownvotedQuestions = models.IntegerField(default=0)
    @save_object_after
    def get_question_downvotes_taken(self):
        self.hisDownvotedQuestions = QuestionRelatedUsers.objects.filter(relatedQuestion__author=self.qandaUser, downvote=True).count()
        return self.hisDownvotedQuestions

    usefulQuestions = models.IntegerField(default=0)
    @save_object_after
    def get_question_usefuls_given(self):
        self.usefulQuestions = QuestionRelatedUsers.objects.filter(relatedUser=self.qandaUser, useful=True).count()
        return self.usefulQuestions

    hisUsefulQuestions = models.IntegerField(default=0)
    @save_object_after
    def get_question_usefuls_taken(self):
        self.hisUsefulQuestions = QuestionRelatedUsers.objects.filter(relatedQuestion__author=self.qandaUser, useful=True).count()
        return self.hisUsefulQuestions

    notUsefulQuestions = models.IntegerField(default=0)
    @save_object_after
    def get_question_notUsefuls_given(self):
        self.notUsefulQuestions = QuestionRelatedUsers.objects.filter(relatedUser=self.qandaUser, notUseful=True).count()
        return self.notUsefulQuestions

    hisNotUsefulQuestions = models.IntegerField(default=0)
    @save_object_after
    def get_question_notUsefuls_taken(self):
        self.hisNotUsefulQuestions = QuestionRelatedUsers.objects.filter(relatedQuestion__author=self.qandaUser, notUseful=True).count()
        return self.hisNotUsefulQuestions

    flaggedQuestions = models.IntegerField(default=0)
    @save_object_after
    def get_question_flags_given(self):
        self.flaggedQuestions = QuestionRelatedUsers.objects.filter(relatedUser=self.qandaUser, flag=True).count()
        return self.flaggedQuestions

    hisFlaggedQuestions = models.IntegerField(default=0)
    @save_object_after
    def get_question_flags_taken(self):
        self.hisFlaggedQuestions = QuestionRelatedUsers.objects.filter(relatedQuestion__author=self.qandaUser, flag=True).count()
        return self.hisFlaggedQuestions

    starredQuestions = models.IntegerField(default=0)
    @save_object_after
    def get_question_stars_given(self):
        self.starredQuestions = QuestionRelatedUsers.objects.filter(relatedUser=self.qandaUser, star=True).count()
        return self.starredQuestions

    hisStarredQuestions = models.IntegerField(default=0)
    @save_object_after
    def get_question_stars_taken(self):
        self.hisStarredQuestions = QuestionRelatedUsers.objects.filter(relatedQuestion__author=self.qandaUser, star=True).count()
        return self.hisStarredQuestions

    upvotedAnswers = models.IntegerField(default=0)
    @save_object_after
    def get_answer_upvotes_given(self):
        self.upvotedAnswers = AnswerRelatedUsers.objects.filter(relatedUser=self.qandaUser, upvote=True).count()
        return self.upvotedAnswers

    hisUpvotedAnswers = models.IntegerField(default=0)
    @save_object_after
    def get_answer_upvotes_taken(self):
        self.hisUpvotedAnswers = AnswerRelatedUsers.objects.filter(relatedAnswer__author=self.qandaUser, upvote=True).count()
        return self.hisUpvotedAnswers

    downvotedAnswers = models.IntegerField(default=0)
    @save_object_after
    def get_answer_downvotes_given(self):
        self.downvotedAnswers = AnswerRelatedUsers.objects.filter(relatedUser=self.qandaUser, downvote=True).count()
        return self.downvotedAnswers

    hisDownvotedAnswers = models.IntegerField(default=0)
    @save_object_after
    def get_answer_downvotes_taken(self):
        self.hisDownvotedAnswers = AnswerRelatedUsers.objects.filter(relatedAnswer__author=self.qandaUser, downvote=True).count()
        return self.hisDownvotedAnswers

    usefulAnswers = models.IntegerField(default=0)
    @save_object_after
    def get_answer_usefuls_given(self):
        self.usefulAnswers = AnswerRelatedUsers.objects.filter(relatedUser=self.qandaUser, useful=True).count()
        return self.usefulAnswers

    hisUsefulAnswers = models.IntegerField(default=0)
    @save_object_after
    def get_answer_usefuls_taken(self):
        self.hisUsefulAnswers = AnswerRelatedUsers.objects.filter(relatedAnswer__author=self.qandaUser, useful=True).count()
        return self.hisUsefulAnswers

    notUsefulAnswers = models.IntegerField(default=0)
    @save_object_after
    def get_answer_notUsefuls_given(self):
        self.notUsefulAnswers = AnswerRelatedUsers.objects.filter(relatedUser=self.qandaUser, notUseful=True).count()
        return self.notUsefulAnswers

    hisNotUsefulAnswers = models.IntegerField(default=0)
    @save_object_after
    def get_answer_notUsefuls_taken(self):
        self.hisNotUsefulAnswers = AnswerRelatedUsers.objects.filter(relatedAnswer__author=self.qandaUser, notUseful=True).count()
        return self.hisNotUsefulAnswers

    flaggedAnswers = models.IntegerField(default=0)
    @save_object_after
    def get_answer_flags_given(self):
        self.flaggedAnswers = AnswerRelatedUsers.objects.filter(relatedUser=self.qandaUser, flag=True).count()
        return self.flaggedAnswers

    hisFlaggedAnswers = models.IntegerField(default=0)
    @save_object_after
    def get_answer_flags_taken(self):
        self.hisFlaggedAnswers = AnswerRelatedUsers.objects.filter(relatedAnswer__author=self.qandaUser, flag=True).count()
        return self.hisFlaggedAnswers

    starredAnswers = models.IntegerField(default=0)
    @save_object_after
    def get_answer_stars_given(self):
        self.starredAnswers = AnswerRelatedUsers.objects.filter(relatedUser=self.qandaUser, star=True).count()
        return self.starredAnswers

    hisStarredAnswers = models.IntegerField(default=0)
    @save_object_after
    def get_answer_stars_taken(self):
        self.hisStarredAnswers = AnswerRelatedUsers.objects.filter(relatedAnswer__author=self.qandaUser, star=True).count()
        return self.hisStarredAnswers

    def synchronize(self):
        self.get_questions()
        self.get_answers()
        self.get_replies()

        self.get_user_stars_given()
        self.get_user_stars_taken()
        self.get_user_flags_given()
        self.get_user_stars_taken()

        self.get_question_upvotes_given()
        self.get_question_upvotes_taken()
        self.get_question_downvotes_given()
        self.get_question_downvotes_taken()
        self.get_question_usefuls_given()
        self.get_question_usefuls_taken()
        self.get_question_notUsefuls_given()
        self.get_question_notUsefuls_taken()
        self.get_question_flags_given()
        self.get_question_flags_taken()
        self.get_question_stars_given()
        self.get_question_stars_taken()

        self.get_answer_upvotes_given()
        self.get_answer_upvotes_taken()
        self.get_answer_downvotes_given()
        self.get_answer_downvotes_taken()
        self.get_answer_usefuls_given()
        self.get_answer_usefuls_taken()
        self.get_answer_notUsefuls_given()
        self.get_answer_notUsefuls_taken()
        self.get_answer_flags_given()
        self.get_answer_flags_taken()
        self.get_answer_stars_given()
        self.get_answer_stars_taken()


    class Meta:
        verbose_name = 'Qanda User Statistic'
        
class QuestionSubscription(notify_models.Subscription):
    question = models.ForeignKey(Question, related_name='subscriptions')
    class Meta:
        verbose_name = 'Question Subscription'
    
class AnswerSubscription(notify_models.Subscription):
    answer = models.ForeignKey(Answer, related_name='subscriptions')
    class Meta:
        verbose_name = 'Answer Subscription'

def createAnswerNotifications(sender, **kwargs):
    created = kwargs['created']
    if created:
        if sender == Answer:
            answer = kwargs['instance']
            Question.objects.subscribe_to_question(answer.question, answer.author, True)
            Answer.objects.subscribe_to_answer(answer, answer.author, True)
            new_notifications = Notification.create_notifications(key='new_answer',
                                                                object_id=str(answer.question.pk),
                                                                message='New answer to '+str(answer.question.title),
                                                                url=reverse('qanda_app.views.question_page', kwargs={'question_id':answer.question.pk,}),
                                                                )
        elif sender == Question:
            question = kwargs['instance']
            Question.objects.subscribe_to_question(question, question.author, True)
        else:
            pass

def createReplyNotifications(sender, **kwargs):
    created = kwargs['created']
    if created:       
        reply = kwargs['instance']
        Answer.objects.subscribe_to_answer(reply.answer, reply.author, True)

    new_notifications = Notification.create_notifications(key='new_reply', 
                                                        object_id=str(reply.answer.pk),
                                                        message='New reply to your answer in '+str(reply.answer.question.title),
                                                        url=reverse('qanda_app.views.question_page', kwargs={'question_id':reply.answer.question.pk,}),
                                                        )
         
           
signals.post_save.connect(createAnswerNotifications, sender=Question)
signals.post_save.connect(createAnswerNotifications, sender=Answer)
signals.post_save.connect(createReplyNotifications, sender=Reply)

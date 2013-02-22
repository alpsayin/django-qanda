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
    def __unicode__(self):
        return u'%d by %s' % (self.pk, self.author.djangoUser)

class Category(models.Model):
    """
        A simple model to hold Question categories such as different sectors
    """
    category = models.CharField(max_length=255, unique=True)
    class Meta:
        verbose_name = "Qanda Category"
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

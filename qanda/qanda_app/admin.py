from django.contrib import admin
from models import QandaUser, Question, Answer, Reply
from models import UserRelations, QuestionRelatedUsers, AnswerRelatedUsers, QandaUserStats

class QandaUserAdmin(admin.ModelAdmin):
	fields = ['djangoUser', 'deleted']
	list_display = ['djangoUser', 'deleted']

class QuestionAdmin(admin.ModelAdmin):
	fields = ['title', 'text', 'author', 'viewCount', 'closeMessage', 'deleted']
	list_display = ['pk','title','author', 'text', 'postDate', 'editDate', 'closeDate','closeMessage', 'closed', 'deleted']
	list_filter = ['postDate', 'editDate', 'closeDate','author']

class AnswerAdmin(admin.ModelAdmin):
	fields = ['text', 'question', 'author']
	list_display = ['pk', 'author', 'text', 'postDate', 'editDate', 'deleted']
	list_filter = ['postDate', 'editDate', 'author']

class ReplyAdmin(admin.ModelAdmin):
	fields = ['text', 'author', 'answer', 'deleted']
	list_display = ['pk', 'author', 'text', 'postDate', 'editDate', 'deleted']
	list_filter = ['postDate', 'editDate', 'author']

class UserRelationsAdmin(admin.ModelAdmin):
	fields = ['relater', 'related', 'star', 'flag']
	list_display = ['relater', 'related', 'star', 'flag']

class QuestionRelatedUsersAdmin(admin.ModelAdmin):
	fields = ['relatedUser', 'relatedQuestion', 'upvote', 'downvote', 'useful', 'notUseful', 'star', 'flag']
	list_display = ['relatedUser', 'relatedQuestion', 'upvote', 'downvote', 'useful', 'notUseful', 'star', 'flag']

class AnswerRelatedUsersAdmin(admin.ModelAdmin):
	fields = ['relatedUser', 'relatedAnswer', 'upvote', 'downvote', 'useful', 'notUseful', 'star', 'flag']
	list_display = ['relatedUser', 'relatedAnswer', 'upvote', 'downvote', 'useful', 'notUseful', 'star', 'flag']

class QandaUserStatsAdmin(admin.ModelAdmin):
	pass

admin.site.register(QandaUser, QandaUserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Reply, ReplyAdmin)

admin.site.register(UserRelations, UserRelationsAdmin)
admin.site.register(QuestionRelatedUsers, QuestionRelatedUsersAdmin)
admin.site.register(AnswerRelatedUsers, AnswerRelatedUsersAdmin)
admin.site.register(QandaUserStats, QandaUserStatsAdmin)
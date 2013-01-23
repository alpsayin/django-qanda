# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AnswerRelatedUsers'
        db.create_table('qanda_app_answerrelatedusers', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('relatedUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qanda_app.QandaUser'])),
            ('relatedQuestion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qanda_app.Answer'])),
            ('upvote', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('downvote', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('useful', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notUseful', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('star', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('qanda_app', ['AnswerRelatedUsers'])

        # Adding model 'QandaUserStats'
        db.create_table('qanda_app_qandauserstats', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('qandaUser', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['qanda_app.QandaUser'], unique=True)),
            ('profileViews', self.gf('django.db.models.fields.IntegerField')()),
            ('uniqueProfileViews', self.gf('django.db.models.fields.IntegerField')()),
            ('questions', self.gf('django.db.models.fields.IntegerField')()),
            ('answers', self.gf('django.db.models.fields.IntegerField')()),
            ('replies', self.gf('django.db.models.fields.IntegerField')()),
            ('tags', self.gf('django.db.models.fields.IntegerField')()),
            ('starredUsers', self.gf('django.db.models.fields.IntegerField')()),
            ('hisStarredUsers', self.gf('django.db.models.fields.IntegerField')()),
            ('upvotedQuestions', self.gf('django.db.models.fields.IntegerField')()),
            ('hisUpvotedQuestions', self.gf('django.db.models.fields.IntegerField')()),
            ('downvotedQuestions', self.gf('django.db.models.fields.IntegerField')()),
            ('hisDownvotedQuestions', self.gf('django.db.models.fields.IntegerField')()),
            ('usefulQuestions', self.gf('django.db.models.fields.IntegerField')()),
            ('hisUsefulQuestions', self.gf('django.db.models.fields.IntegerField')()),
            ('notUsefulQuestions', self.gf('django.db.models.fields.IntegerField')()),
            ('hisNotUsefulQuestions', self.gf('django.db.models.fields.IntegerField')()),
            ('flaggedQuestions', self.gf('django.db.models.fields.IntegerField')()),
            ('hisFlaggedQuestions', self.gf('django.db.models.fields.IntegerField')()),
            ('starredQuestions', self.gf('django.db.models.fields.IntegerField')()),
            ('hisStarredQuestions', self.gf('django.db.models.fields.IntegerField')()),
            ('upvotedAnswers', self.gf('django.db.models.fields.IntegerField')()),
            ('hisUpvotedAnswers', self.gf('django.db.models.fields.IntegerField')()),
            ('downvotedAnswers', self.gf('django.db.models.fields.IntegerField')()),
            ('hisDownvotedAnswers', self.gf('django.db.models.fields.IntegerField')()),
            ('usefulAnswers', self.gf('django.db.models.fields.IntegerField')()),
            ('hisUsefulAnswers', self.gf('django.db.models.fields.IntegerField')()),
            ('notUsefulAnswers', self.gf('django.db.models.fields.IntegerField')()),
            ('hisNotUsefulAnswers', self.gf('django.db.models.fields.IntegerField')()),
            ('flaggedAnswers', self.gf('django.db.models.fields.IntegerField')()),
            ('hisFlaggedAnswers', self.gf('django.db.models.fields.IntegerField')()),
            ('starredAnswers', self.gf('django.db.models.fields.IntegerField')()),
            ('hisStarredAnswers', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('qanda_app', ['QandaUserStats'])

        # Adding model 'Reply'
        db.create_table('qanda_app_reply', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='replies', to=orm['qanda_app.QandaUser'])),
            ('postDate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('editDate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('qanda_app', ['Reply'])

        # Adding model 'Answer'
        db.create_table('qanda_app_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['qanda_app.Question'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['qanda_app.QandaUser'])),
            ('postDate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('editDate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('qanda_app', ['Answer'])

        # Adding model 'QuestionRelatedUsers'
        db.create_table('qanda_app_questionrelatedusers', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('relatedUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qanda_app.QandaUser'])),
            ('relatedQuestion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qanda_app.Question'])),
            ('upvote', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('downvote', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('useful', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notUseful', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('star', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('qanda_app', ['QuestionRelatedUsers'])

        # Adding model 'QandaUser'
        db.create_table('qanda_app_qandauser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('djangoUser', self.gf('django.db.models.fields.related.OneToOneField')(related_name='QandaUser', unique=True, to=orm['auth.User'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('qanda_app', ['QandaUser'])

        # Adding model 'UserStars'
        db.create_table('qanda_app_userstars', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('starrer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='starrer_relations', to=orm['qanda_app.QandaUser'])),
            ('starred', self.gf('django.db.models.fields.related.ForeignKey')(related_name='starred_relations', to=orm['qanda_app.QandaUser'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('qanda_app', ['UserStars'])

        # Adding model 'Question'
        db.create_table('qanda_app_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', to=orm['qanda_app.QandaUser'])),
            ('viewCount', self.gf('django.db.models.fields.IntegerField')()),
            ('uniqueViewCount', self.gf('django.db.models.fields.IntegerField')()),
            ('postDate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('editDate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('closeMessage', self.gf('django.db.models.fields.TextField')()),
            ('closeDate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('qanda_app', ['Question'])


    def backwards(self, orm):
        # Deleting model 'AnswerRelatedUsers'
        db.delete_table('qanda_app_answerrelatedusers')

        # Deleting model 'QandaUserStats'
        db.delete_table('qanda_app_qandauserstats')

        # Deleting model 'Reply'
        db.delete_table('qanda_app_reply')

        # Deleting model 'Answer'
        db.delete_table('qanda_app_answer')

        # Deleting model 'QuestionRelatedUsers'
        db.delete_table('qanda_app_questionrelatedusers')

        # Deleting model 'QandaUser'
        db.delete_table('qanda_app_qandauser')

        # Deleting model 'UserStars'
        db.delete_table('qanda_app_userstars')

        # Deleting model 'Question'
        db.delete_table('qanda_app_question')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'qanda_app.answer': {
            'Meta': {'object_name': 'Answer'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['qanda_app.QandaUser']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['qanda_app.Question']"}),
            'relatedUsers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_answers'", 'symmetrical': 'False', 'through': "orm['qanda_app.AnswerRelatedUsers']", 'to': "orm['qanda_app.QandaUser']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'qanda_app.answerrelatedusers': {
            'Meta': {'object_name': 'AnswerRelatedUsers'},
            'downvote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notUseful': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'relatedQuestion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qanda_app.Answer']"}),
            'relatedUser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qanda_app.QandaUser']"}),
            'star': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'upvote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'useful': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'qanda_app.qandauser': {
            'Meta': {'object_name': 'QandaUser'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'djangoUser': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'QandaUser'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'starred': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'starred_by'", 'null': 'True', 'through': "orm['qanda_app.UserStars']", 'to': "orm['qanda_app.QandaUser']"})
        },
        'qanda_app.qandauserstats': {
            'Meta': {'object_name': 'QandaUserStats'},
            'answers': ('django.db.models.fields.IntegerField', [], {}),
            'downvotedAnswers': ('django.db.models.fields.IntegerField', [], {}),
            'downvotedQuestions': ('django.db.models.fields.IntegerField', [], {}),
            'flaggedAnswers': ('django.db.models.fields.IntegerField', [], {}),
            'flaggedQuestions': ('django.db.models.fields.IntegerField', [], {}),
            'hisDownvotedAnswers': ('django.db.models.fields.IntegerField', [], {}),
            'hisDownvotedQuestions': ('django.db.models.fields.IntegerField', [], {}),
            'hisFlaggedAnswers': ('django.db.models.fields.IntegerField', [], {}),
            'hisFlaggedQuestions': ('django.db.models.fields.IntegerField', [], {}),
            'hisNotUsefulAnswers': ('django.db.models.fields.IntegerField', [], {}),
            'hisNotUsefulQuestions': ('django.db.models.fields.IntegerField', [], {}),
            'hisStarredAnswers': ('django.db.models.fields.IntegerField', [], {}),
            'hisStarredQuestions': ('django.db.models.fields.IntegerField', [], {}),
            'hisStarredUsers': ('django.db.models.fields.IntegerField', [], {}),
            'hisUpvotedAnswers': ('django.db.models.fields.IntegerField', [], {}),
            'hisUpvotedQuestions': ('django.db.models.fields.IntegerField', [], {}),
            'hisUsefulAnswers': ('django.db.models.fields.IntegerField', [], {}),
            'hisUsefulQuestions': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notUsefulAnswers': ('django.db.models.fields.IntegerField', [], {}),
            'notUsefulQuestions': ('django.db.models.fields.IntegerField', [], {}),
            'profileViews': ('django.db.models.fields.IntegerField', [], {}),
            'qandaUser': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['qanda_app.QandaUser']", 'unique': 'True'}),
            'questions': ('django.db.models.fields.IntegerField', [], {}),
            'replies': ('django.db.models.fields.IntegerField', [], {}),
            'starredAnswers': ('django.db.models.fields.IntegerField', [], {}),
            'starredQuestions': ('django.db.models.fields.IntegerField', [], {}),
            'starredUsers': ('django.db.models.fields.IntegerField', [], {}),
            'tags': ('django.db.models.fields.IntegerField', [], {}),
            'uniqueProfileViews': ('django.db.models.fields.IntegerField', [], {}),
            'upvotedAnswers': ('django.db.models.fields.IntegerField', [], {}),
            'upvotedQuestions': ('django.db.models.fields.IntegerField', [], {}),
            'usefulAnswers': ('django.db.models.fields.IntegerField', [], {}),
            'usefulQuestions': ('django.db.models.fields.IntegerField', [], {})
        },
        'qanda_app.question': {
            'Meta': {'object_name': 'Question'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': "orm['qanda_app.QandaUser']"}),
            'closeDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'closeMessage': ('django.db.models.fields.TextField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'relatedUsers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_questions'", 'symmetrical': 'False', 'through': "orm['qanda_app.QuestionRelatedUsers']", 'to': "orm['qanda_app.QandaUser']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uniqueViewCount': ('django.db.models.fields.IntegerField', [], {}),
            'viewCount': ('django.db.models.fields.IntegerField', [], {})
        },
        'qanda_app.questionrelatedusers': {
            'Meta': {'object_name': 'QuestionRelatedUsers'},
            'downvote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notUseful': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'relatedQuestion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qanda_app.Question']"}),
            'relatedUser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qanda_app.QandaUser']"}),
            'star': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'upvote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'useful': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'qanda_app.reply': {
            'Meta': {'object_name': 'Reply'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replies'", 'to': "orm['qanda_app.QandaUser']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'qanda_app.userstars': {
            'Meta': {'object_name': 'UserStars'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'starred': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'starred_relations'", 'to': "orm['qanda_app.QandaUser']"}),
            'starrer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'starrer_relations'", 'to': "orm['qanda_app.QandaUser']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['qanda_app']
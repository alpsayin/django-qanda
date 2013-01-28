# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Category', fields ['category']
        db.create_unique('qanda_app_category', ['category'])


    def backwards(self, orm):
        # Removing unique constraint on 'Category', fields ['category']
        db.delete_unique('qanda_app_category', ['category'])


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
            'editDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'relatedAnswer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_relation'", 'to': "orm['qanda_app.Answer']"}),
            'relatedUser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answer_relation'", 'to': "orm['qanda_app.QandaUser']"}),
            'star': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'upvote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'useful': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'qanda_app.category': {
            'Meta': {'object_name': 'Category'},
            'category': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'qanda_app.qandauser': {
            'Meta': {'object_name': 'QandaUser'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'djangoUser': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'QandaUser'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relatedUsers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'relaterUsers'", 'symmetrical': 'False', 'through': "orm['qanda_app.UserRelations']", 'to': "orm['qanda_app.QandaUser']"})
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
            'upvotedAnswers': ('django.db.models.fields.IntegerField', [], {}),
            'upvotedQuestions': ('django.db.models.fields.IntegerField', [], {}),
            'usefulAnswers': ('django.db.models.fields.IntegerField', [], {}),
            'usefulQuestions': ('django.db.models.fields.IntegerField', [], {})
        },
        'qanda_app.question': {
            'Meta': {'object_name': 'Question'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': "orm['qanda_app.QandaUser']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qanda_app.Category']", 'null': 'True'}),
            'closeDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'closeMessage': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'relatedUsers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_questions'", 'symmetrical': 'False', 'through': "orm['qanda_app.QuestionRelatedUsers']", 'to': "orm['qanda_app.QandaUser']"}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'viewCount': ('django.db.models.fields.IntegerField', [], {})
        },
        'qanda_app.questionrelatedusers': {
            'Meta': {'object_name': 'QuestionRelatedUsers'},
            'downvote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notUseful': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'relatedQuestion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_relation'", 'to': "orm['qanda_app.Question']"}),
            'relatedUser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'question_relation'", 'to': "orm['qanda_app.QandaUser']"}),
            'star': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'upvote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'useful': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'qanda_app.reply': {
            'Meta': {'object_name': 'Reply'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replies'", 'null': 'True', 'to': "orm['qanda_app.Answer']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replies'", 'to': "orm['qanda_app.QandaUser']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'qanda_app.userrelations': {
            'Meta': {'object_name': 'UserRelations'},
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'related': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relatedRelation'", 'to': "orm['qanda_app.QandaUser']"}),
            'relater': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relaterRelation'", 'to': "orm['qanda_app.QandaUser']"}),
            'star': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['qanda_app']
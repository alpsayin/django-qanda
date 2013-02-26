# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Category.category'
        db.delete_column('qanda_app_category', 'category')

        # Adding field 'Category.name'
        db.add_column('qanda_app_category', 'name',
                      self.gf('django.db.models.fields.CharField')(default='HVAC', unique=True, max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Category.category'
        db.add_column('qanda_app_category', 'category',
                      self.gf('django.db.models.fields.CharField')(default='HVAC', max_length=255, unique=True),
                      keep_default=False)

        # Deleting field 'Category.name'
        db.delete_column('qanda_app_category', 'name')


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
        'django_notify.notification': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Notification', 'db_table': "'notify_notification'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_emailed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'occurrences': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_notify.Subscription']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'django_notify.notificationtype': {
            'Meta': {'object_name': 'NotificationType', 'db_table': "'notify_notificationtype'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'django_notify.settings': {
            'Meta': {'object_name': 'Settings', 'db_table': "'notify_settings'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'django_notify.subscription': {
            'Meta': {'object_name': 'Subscription', 'db_table': "'notify_subscription'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'latest_for'", 'null': 'True', 'to': "orm['django_notify.Notification']"}),
            'notification_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_notify.NotificationType']"}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'send_emails': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_notify.Settings']"})
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
        'qanda_app.answersubscription': {
            'Meta': {'object_name': 'AnswerSubscription', '_ormbases': ['django_notify.Subscription']},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'to': "orm['qanda_app.Answer']"}),
            'subscription_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['django_notify.Subscription']", 'unique': 'True', 'primary_key': 'True'})
        },
        'qanda_app.category': {
            'Meta': {'object_name': 'Category'},
            'about': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'qanda_app.qandauser': {
            'Meta': {'object_name': 'QandaUser'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'djangoUser': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'QandaUser'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relatedUsers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'relaterUsers'", 'symmetrical': 'False', 'through': "orm['qanda_app.UserRelations']", 'to': "orm['qanda_app.QandaUser']"})
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
            'viewCount': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
        'qanda_app.questionsubscription': {
            'Meta': {'object_name': 'QuestionSubscription', '_ormbases': ['django_notify.Subscription']},
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'to': "orm['qanda_app.Question']"}),
            'subscription_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['django_notify.Subscription']", 'unique': 'True', 'primary_key': 'True'})
        },
        'qanda_app.reply': {
            'Meta': {'object_name': 'Reply'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replies'", 'null': 'True', 'to': "orm['qanda_app.Answer']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replies'", 'to': "orm['qanda_app.QandaUser']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''"})
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
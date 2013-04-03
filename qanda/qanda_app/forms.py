from django.forms import ModelForm, Textarea, TextInput, Select
from models import Question, Answer, Reply
from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _


class QuestionForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(QuestionForm, self).__init__(*args, **kwargs)
		self.fields['category'].required = False

	class Meta:
		model = Question
		fields = ('title', 'category', 'text', 'tags')
		widgets = {
			'title': TextInput(attrs={'size': 220, 'class':'span8'}),
			'category' : Select(attrs={'class':'span7'},),
			'text': Textarea(attrs={'cols': 120, 'rows': 16, 'class':'span8'}),
			# 'tags': TextInput(attrs={'size': 220, 'class':'span8'}),
		}

class QuestionCloseForm(forms.Form):
	message = forms.CharField(max_length=511, widget=Textarea(attrs={'rows': 10, 'id':'questionCloseForm',}), initial=_("This question is closed by the administrators. ")+getattr(settings, 'ROOT_URL', 'http://127.0.0.1:8000/qanda'))

class AnswerForm(ModelForm):
	class Meta:
		model = Answer
		fields = ( 'text', )
		widgets = {
			'text': Textarea(attrs={'cols': 120, 'rows': 10, 'class':'span8'}),
		}

class ReplyForm(ModelForm):
	class Meta:
		model = Reply
		fields = ( 'text', )
		widgets = {
			'text': Textarea(attrs={'cols': 120, 'rows': 2, 'class':'span7'}),
		}

class  SubscriptionForm(forms.Form):
	subscribed = forms.BooleanField(initial=False)
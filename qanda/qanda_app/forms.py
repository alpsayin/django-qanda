from django.forms import ModelForm, Textarea, TextInput, Select
from models import Question, Answer, Reply
from django import forms


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
			'text': Textarea(attrs={'cols': 120, 'rows': 20, 'class':'span8'}),
			'tags': TextInput(attrs={'size': 220, 'class':'span8'}),
		}

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
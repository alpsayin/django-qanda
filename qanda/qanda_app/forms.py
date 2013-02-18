from django.forms import ModelForm, Textarea, TextInput
from models import Question, Answer, Reply
from django import forms


class QuestionForm(ModelForm):
	class Meta:
		model = Question
		fields = ('title', 'text', 'tags')
		widgets = {
			'title': TextInput(attrs={'size': 220, 'class':'span8'}),
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
			'text': Textarea(attrs={'cols': 80, 'rows': 2, 'class':'span6'}),
		}

class  SubscriptionForm(forms.Form):
	subscribed = forms.BooleanField(initial=False)
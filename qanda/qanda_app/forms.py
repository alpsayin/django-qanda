from django.forms import ModelForm, Textarea
from models import Question, Answer, Reply

class QuestionForm(ModelForm):
	class Meta:
		model = Question
		fields = ('title', 'text', 'tags')

class AnswerForm(ModelForm):
	class Meta:
		model = Answer
		fields = ( 'text', )
		widgets = {
			'text': Textarea(attrs={'cols': 80, 'rows': 10}),
		}

class ReplyForm(ModelForm):
	class Meta:
		model = Reply
		fields = ( 'text', )
		widgets = {
			'text': Textarea(attrs={'cols': 80, 'rows': 2}),
		}
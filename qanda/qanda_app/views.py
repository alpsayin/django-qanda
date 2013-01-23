# Create your views here.
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from models import Question

def index(request):
	return HttpResponse("questions index")

class QuestionView(TemplateView):
	template_name = 'question.html'

	def get_context_data(self, **kwargs):
		context = super(QuestionView, self).get_context_data(**kwargs)
		question = get_object_or_404(Question, pk=kwargs['question_id'])
		answers = question.answers.all()
		context['question'] = question
		context['answers'] = answers
		return context
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.aggregates import Max
from django.middleware.csrf import _sanitize_token
from django.utils.crypto import constant_time_compare
from django.utils.http import same_origin
from tastypie import fields
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from models import QandaUser, Question, Answer, Reply

class SessionAuthentication(Authentication):
	"""
	An authentication mechanism that piggy-backs on Django sessions.

	This is useful when the API is talking to Javascript on the same site.
	Relies on the user being logged in through the standard Django login
	setup.

	Requires a valid CSRF token.
	"""
	def is_authenticated(self, request, **kwargs):
		"""
		Checks to make sure the user is logged in & has a Django session.
		"""
		# Cargo-culted from Django 1.3/1.4's ``django/middleware/csrf.py``.
		# We can't just use what's there, since the return values will be
		# wrong.
		# We also can't risk accessing ``request.POST``, which will break with
		# the serialized bodies.
		if request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
			return request.user.is_authenticated()

		if getattr(request, '_dont_enforce_csrf_checks', False):
			return request.user.is_authenticated()

		csrf_token = _sanitize_token(request.COOKIES.get(settings.CSRF_COOKIE_NAME, ''))

		if request.is_secure():
			referer = request.META.get('HTTP_REFERER')

			if referer is None:
				return False

			good_referer = 'https://%s/' % request.get_host()

			if not same_origin(referer, good_referer):
				return False

		request_csrf_token = request.META.get('HTTP_X_CSRFTOKEN', '')

		if not constant_time_compare(request_csrf_token, csrf_token):
			return False

		return request.user.is_authenticated()

	def get_identifier(self, request):
		"""
		Provides a unique string identifier for the requestor.

		This implementation returns the user's username.
		"""
		return request.user.username

class UserAuthorization(DjangoAuthorization):
	def is_authorized(self, request, object=None):
		return super(UserAuthorization, self).is_authorized(request,object)
    
	def apply_limits(self,request,object_list):
		return object_list

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		authentication=SessionAuthentication()
		authorization = UserAuthorization()
		fields = ['username']
		list_allowed_methods = ['get']
		detail_allowed_methods = ['get','put','patch']
		filtering = {
			'username': ALL ,
		}
        
	def determine_format(self, request): 
		return "application/json"
             
	def dehydrate(self, bundle):
		userInstance=bundle.obj
        
		#if self.get_resource_uri(bundle) == bundle.request.path:
			#"Detail"
		if bundle.request.user.pk == bundle.obj.pk:
			bundle.data['first-name']=userInstance.first_name
			bundle.data['last-name']=userInstance.last_name
			bundle.data['email']=userInstance.email
		return bundle 
            
	def apply_authorization_limits(self, request, object_list):
		if request.method in ["PUT","PATCH"]:
			return object_list.filter(pk=request.user.pk)
		else:
			return object_list

class QandaUserResource(ModelResource):
	djangoUser = fields.ForeignKey(UserResource, 'djangoUser')
	class Meta:
		queryset = QandaUser.objects.all()
		resource_name = 'qandauser'
		list_allowed_methods = ['get']
		detail_allowed_methods = ['get','put','patch']
		authentication = SessionAuthentication()
		authorization = UserAuthorization()    
		always_return_data=True
		filtering = {
			'djangoUser': ALL_WITH_RELATIONS ,
		}
	def determine_format(self, request): 
		return "application/json" 

class QuestionResource(ModelResource):
	author = fields.ForeignKey(QandaUserResource, 'author')
	class Meta:
		queryset = Question.objects.all()
		resource_name = 'question'
		list_allowed_methods = ['get']
		detail_allowed_methods = ['get','put','patch']
		authentication = SessionAuthentication()
		authorization = UserAuthorization()    
		always_return_data=True
		filtering = {
			'djangoUser': ALL_WITH_RELATIONS ,
		}
	def determine_format(self, request): 
		return "application/json" 

class AnswerResource(ModelResource):
	author = fields.ForeignKey(QandaUserResource, 'author')
	question = fields.ForeignKey(QuestionResource, 'question')
	class Meta:
		queryset = Answer.objects.all()
		resource_name = 'answer'
		list_allowed_methods = ['get']
		detail_allowed_methods = ['get','put','patch']
		authentication = SessionAuthentication()
		authorization = UserAuthorization()    
		always_return_data=True
		filtering = {
			'djangoUser': ALL_WITH_RELATIONS ,
		}
	def determine_format(self, request): 
		return "application/json" 

class ReplyResource(ModelResource):
	author = fields.ForeignKey(QandaUserResource, 'author')
	answer = fields.ForeignKey(AnswerResource, 'answer')
	class Meta:
		queryset = Reply.objects.all()
		resource_name = 'reply'
		list_allowed_methods = ['get']
		detail_allowed_methods = ['get','put','patch']
		authentication = SessionAuthentication()
		authorization = UserAuthorization()    
		always_return_data=True
		filtering = {
			'djangoUser': ALL_WITH_RELATIONS ,
		}
	def determine_format(self, request): 
		return "application/json" 

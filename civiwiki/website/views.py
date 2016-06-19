import json

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from api.models import Category, Account, Topic

from legislation import sunlightapi as sun
from utils.custom_decorators import beta_blocker, login_required

@login_required
@beta_blocker
def account_home(request):
	a = Account.objects.get(user=request.user)
	friend_data_dictionary = Account.objects.friends(a)

	return TemplateResponse(request, 'home.html',
			dict(friends=friend_data_dictionary['friends'],
				requests=friend_data_dictionary['requests'],
				profile=Account.objects.summarize(a),
				legislator=sun.get_legislator_and_district(a),
				bills=sun.get_bill_information(a)))

@login_required
@beta_blocker
def create_group(request):
	return TemplateResponse(request, 'newgroup.html', {})

@login_required
@beta_blocker
def dbview(request):
	result = [{'id': c.id, 'name': c.name} for c in Category.objects.all()]

	return TemplateResponse(request, 'dbview.html', {'result': json.dumps(result)})

@login_required
@beta_blocker
def add_civi(request):
	categories = [{'id': c.id, 'name': c.name} for c in Category.objects.all()]
	topics = [{'id': c.id, 'topic': c.topic} for c in Topic.objects.all()]

	return TemplateResponse(request, 'add_civi.html', {'categories': json.dumps(categories), 'topics': json.dumps(topics)})

def login_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')

	return TemplateResponse(request, 'login.html', {})

def beta_view(request):
	return TemplateResponse(request, 'beta_blocker.html', {})

def declaration(request):
	return TemplateResponse(request, 'declaration.html', {})

def about_view(request):
	return TemplateResponse(request, 'about.html', {})

def support_us_view(request):
	return TemplateResponse(request, 'supportus.html', {})

def does_not_exist(request):
	return TemplateResponse(request, '404.html', {})

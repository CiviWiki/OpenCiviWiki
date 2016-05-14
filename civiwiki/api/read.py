from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from utils.custom_decorators import require_post_params
from django.db.models import Q
from models import Account, Topic, Attachment, Category, Civi, Comment, Hashtag
import sys, json, random, hashlib


# Create your views here.
@require_post_params(params=['id'])
def topTen(request):
	'''
		Given an topic ID, returns the top ten Civis of type Issue
		(the chain heads)
	'''
	topic_id = request.POST.get('id', -1)
	try:
		topic = Topic.objects.get(id=int(topic_id))
		return JsonResponse({'result':Civi.objects.block(topic)})
	except Topic.DoesNotExist as e:
		return HttpResponseBadRequest(reason=str(e))

def getCategories(request):
	'''
		Returns to user list of all Categories
	'''
	result = [{'id': c.id, 'name': c.name} for c in Category.objects.all()]
	return JsonResponse({"result":result})

@require_post_params(params=['id'])
def getTopics(request):
	'''
		Takes in a category ID, returns a list of topics under the category.
	'''
	category_id = request.POST.get('id', -1)

	try:
		Category.objects.get(id=category_id)
	except Category.DoesNotExist as e:
		return HttpResponseBadRequest(reason=str(e))

	result = [{'id':a.id, 'topic': a.topic, 'bill': a.bill} for a in Topic.objects.filter(category_id=category_id)]
	return JsonResponse({"result":result})


@require_post_params(params=['id'])
def getUser(request):
	'''
		Takes in a user ID, returns a user object.
	'''
	try:
		a = Account.objects.get(id=request.POST.get("id", -1))
		return JsonResponse({"result":Account.objects.serialize(a)})
	except Account.DoesNotExist as e:
		return HttpResponseBadRequest(reason=str(e))

@require_post_params(params=['username'])
def getIdByUsername(request):
	'''
	takes in username and responds with an accountid

	image fields are going to be urls in which you can access as base.com/media/<image_url>

	:param request: with username
	:return: user object
	'''
	try:
		username = request.POST.get("username", False)
		return JsonResponse({"result": Account.objects.get(user__username=username).id})
	except Account.DoesNotExist as e:
		return HttpResponseBadRequest(reason=str(e))

@require_post_params(params=['id'])
def getCivi(request):
	'''
		takes in a civi ID and returns a civi and all its descendents.
	'''
	id = request.POST.get("id", -1)
	try:
		c = Civi.objects.get(id=id)
		return JsonResponse({"result":json.dumps(Civi.objects.serialize(c))})
	except Civi.DoesNotExist as e:
		return HttpResponseBadRequest(reason=str(e))


@require_post_params(params=['id'])
def getBlock(request):
	topic_id = request.POST.get("id", -1)
	try:
		topic = Topic.objects.get(id=topic_id)
		start = int(request.POST.get("start", 0))
		end = int(request.POST.get("end", 0))
		if start < 0 or end < 0 or end < start:
			raise Exception("Invalid start or end parameters.")
		return JsonResponse({"result":Civi.objects.block(topic, start, end)})
	except Topic.DoesNotExist as e:
		return HttpResponseBadRequest(reason=str(e))
	except Exception as e:
		return HttpResponseBadRequest(reason=str(e))

import sys, json, random, hashlib

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from models import Account, Topic, Attachment, Category, Civi, Comment, Hashtag, Thread
from django.contrib.auth.models import User
from utils.custom_decorators import require_post_params
from legislation import sunlightapi as sun


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


def getUser(request, user):
    try:
        u = User.objects.get(username=user)
        a = Account.objects.get(user=u)

        return JsonResponse(Account.objects.summarize(a))
    except Account.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))

def getThread(request, thread_id):
    try:
        t = Thread.objects.filter(id=thread_id)
        t = {
            'title': 'Police Use of Deadly Force',
            'category': 'Public Safety',
            'topic': 'Policing',
            'summary': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            'facts': ['sdlkfjhklsdklfu sldjf klssdfsdfssdf sdf sdfsd dfssdf dfsdfsdfs dfsdfsd', 'sdlkfhjsdf sdf sdf sdfsdfsd  sd', 'sldksdfsd sdf sdf sdf sdf fjhlksd', 'sdlkfhjsdsdfsdfsdf sdf sd  fsdf sdf sdfsdf sd sdff sdf sdf sdfsdfsd  sd', 'sldksdfsd sdf sdf sdf sdf fjhlksd'],
            'contributors': ['dsd sdfsd sd sdan', 'darius', 'yo mamsd dsd sd sd sd a', '4', '5', '6', '7', '8', '9', '10'],
            'num_views': '243',
            'num_civis': '17',
            'num_responses': '42',
            'problems': [{'type': 'problem', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'problem', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'problem', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'problem', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'problem', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}],
            'causes': [{'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}],
            'solutions': [{'type': 'solution', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'solution', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'solution', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'type': 'solution', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}]
        }

        return JsonResponse(t)
    except Exception as e:
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

from django.http import JsonResponse, HttpResponseBadRequest
from models import Account, Thread, Civi
#  Topic, Attachment, Category, Civi, Comment, Hashtag,
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from utils import json_response
import json
# from utils.custom_decorators import require_post_params
# from legislation import sunlightapi as sun


# # Create your views here.
# @require_post_params(params=['id'])
# def topTen(request):
# 	'''
# 		Given an topic ID, returns the top ten Civis of type Issue
# 		(the chain heads)
# 	'''
# 	topic_id = request.POST.get('id', -1)
# 	try:
# 		topic = Topic.objects.get(id=int(topic_id))
# 		return JsonResponse({'result':Civi.objects.block(topic)})
# 	except Topic.DoesNotExist as e:
# 		return HttpResponseBadRequest(reason=str(e))
#
# def getCategories(request):
# 	'''
# 		Returns to user list of all Categories
# 	'''
# 	result = [{'id': c.id, 'name': c.name} for c in Category.objects.all()]
# 	return JsonResponse({"result":result})
#
# @require_post_params(params=['id'])
# def getTopics(request):
# 	'''
# 		Takes in a category ID, returns a list of topics under the category.
# 	'''
# 	category_id = request.POST.get('id', -1)
#
# 	try:
# 		Category.objects.get(id=category_id)
# 	except Category.DoesNotExist as e:
# 		return HttpResponseBadRequest(reason=str(e))
#
# 	result = [{'id':a.id, 'topic': a.topic, 'bill': a.bill} for a in Topic.objects.filter(category_id=category_id)]
# 	return JsonResponse({"result":result})


def get_user(request, user):
    try:
        u = User.objects.get(username=user)
        a = Account.objects.get(user=u)

        return JsonResponse(model_to_dict(a))
    except Account.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))

def get_profile(request, user):
    try:
        u = User.objects.get(username=user)
        a = Account.objects.get(user=u)
        result = Account.objects.summarize(a)

        reps = ['W000812', 'C001049', 'B000575', 'M001170']
        rep_list = []
        for rep in reps:
            json_data = open('fixtures/data/{}.json'.format(rep))
            data = json.load(json_data)
            r = dict(
                profile_image = "https://theunitedstates.io/images/congress/450x550/{}.jpg".format(rep),
                username= rep,
                title= data['title'],
                first_name= data['first_name'],
                last_name= data['last_name'],
                party= "Republican" if data['party']=="R" else "Democrat",
                alignment= 0
            )
            json_data.close()
            rep_list.append(json.dumps(r))

        result['representatives'] = rep_list
        result['issues'] = ['''{"category": "category", "issue":"Example Issue that the User probably cares about" }''']*20
        return JsonResponse(result)

    except Account.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))

def get_thread(request, thread_id):
    try:
        t = Thread.objects.get(id=thread_id)
        civis = Civi.objects.filter(thread_id=thread_id).values()
        problems = civis.filter(c_type='problem')
        causes = civis.filter(c_type='cause')
        solutions = civis.filter(c_type='solution')
        data = {
            'title': t.title,
            'summary': t.summary,
            'hashtags': t.hashtags.all().values(),
            'author': model_to_dict(t.author),
            'category': model_to_dict(t.category),
            'created': t.created,
            'problems': problems,
            'causes': causes,
            'solutions': solutions,
            'contributors': Account.objects.all().values(),
            'num_civis': len(civis),
        }
        # t = {
        #     'title': 'Police Use of Deadly Force',
        #     'category': 'Public Safety',
        #     'topic': 'Policing',
        #     'summary': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        #     'facts': ['sdlkfjhklsdklfu sldjf klssdfsdfssdf sdf sdfsd dfssdf dfsdfsdfs dfsdfsd', 'sdlkfhjsdf sdf sdf sdfsdfsd  sd', 'sldksdfsd sdf sdf sdf sdf fjhlksd', 'sdlkfhjsdsdfsdfsdf sdf sd  fsdf sdf sdfsdf sd sdff sdf sdf sdfsdfsd  sd', 'sldksdfsd sdf sdf sdf sdf fjhlksd'],
        #     'contributors': ['dsd sdfsd sd sdan', 'darius', 'yo mamsd dsd sd sd sd a', '4', '5', '6', '7', '8', '9', '10'],
        #     'num_views': '243',
        #     'num_civis': '17',
        #     'num_responses': '42',
        #     'problems': [{'id': 'one', 'type': 'problem', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'two', 'type': 'problem', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'three', 'type': 'problem', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'four', 'type': 'problem', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'five', 'type': 'problem', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}],
        #     'causes': [{'id': 'six', 'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'seven', 'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'eight', 'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'nine', 'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'ten', 'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'eleven', 'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'twelve', 'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'thirteen', 'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'fourteen', 'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'fifteen', 'type': 'cause', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}],
        #     'solutions': [{'id': 'sixteen', 'type': 'solution', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'seventeen', 'type': 'solution', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'eighteen', 'type': 'solution', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'nineteen', 'type': 'solution', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}]
        # }

        return json_response(data)
    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))

def get_responses(request, thread_id, civi_id):
    try:
        t = Thread.objects.filter(id=thread_id)
        t = [{'id': 'one', 'type': 'response', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'two', 'type': 'response', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'three', 'type': 'response', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'four', 'type': 'response', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}, {'id': 'five', 'type': 'response', 'title': 'Use of deadly force against the mentally ill people', 'body': 'Amnesty International noted the problem of police using deadly force against mentally ill or disturbed people who could have been subdued through less extreme measures. Further cases have been reported since then, including suicidal individuals shot by police after they had harmed themselves but not attacked other people. For example, in February 1999 Ricardo Clos is reported to have died after being shot at 38 times by Los Angeles sheriffs deputies who had responded to a call for help from his wife after he had cut himself in the neck. Police reportedly opened fire after he threw the knife towards them (missing them).', 'attachments': ['hi', 'hello'], 'author': 'Author Name', 'created': 'September 20, 2016'}]

        return JsonResponse(t, safe=False)
    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))

# @require_post_params(params=['username'])
# def getIdByUsername(request):
# 	'''
# 	takes in username and responds with an accountid
#
# 	image fields are going to be urls in which you can access as base.com/media/<image_url>
#
# 	:param request: with username
# 	:return: user object
# 	'''
# 	try:
# 		username = request.POST.get("username", False)
# 		return JsonResponse({"result": Account.objects.get(user__username=username).id})
# 	except Account.DoesNotExist as e:
# 		return HttpResponseBadRequest(reason=str(e))
#
# @require_post_params(params=['id'])
# def getCivi(request):
# 	'''
# 		takes in a civi ID and returns a civi and all its descendents.
# 	'''
# 	id = request.POST.get("id", -1)
# 	try:
# 		c = Civi.objects.get(id=id)
# 		return JsonResponse({"result":json.dumps(Civi.objects.serialize(c))})
# 	except Civi.DoesNotExist as e:
# 		return HttpResponseBadRequest(reason=str(e))
#
#
# @require_post_params(params=['id'])
# def getBlock(request):
# 	topic_id = request.POST.get("id", -1)
# 	try:
# 		topic = Topic.objects.get(id=topic_id)
# 		start = int(request.POST.get("start", 0))
# 		end = int(request.POST.get("end", 0))
# 		if start < 0 or end < 0 or end < start:
# 			raise Exception("Invalid start or end parameters.")
# 		return JsonResponse({"result":Civi.objects.block(topic, start, end)})
# 	except Topic.DoesNotExist as e:
# 		return HttpResponseBadRequest(reason=str(e))
# 	except Exception as e:
# 		return HttpResponseBadRequest(reason=str(e))

from django.http import JsonResponse, HttpResponseBadRequest
from models import Account, Thread, Civi, Representative, Category, Activity
#  Topic, Attachment, Category, Civi, Comment, Hashtag,
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from utils import json_response
import json
# from utils.custom_decorators import require_post_params
from legislation import sunlightapi as sun


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

def get_card(request, user):
    try:
        u = User.objects.get(username=user)
        a = Account.objects.get(user=u)
        result = Account.objects.card_summarize(a, Account.objects.get(user=request.user))
        return JsonResponse(result)
    except Account.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))
    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))

def get_profile(request, user):
    try:
        u = User.objects.get(username=user)
        a = Account.objects.get(user=u)
        result = Account.objects.summarize(a)
        # result = {}

        result['representatives'] = []
        # result['issues'] = ['''{"category": "category", "issue":"Example Issue that the User probably cares about" }''']*20

        result['issues'] = []
        voted_solutions = Activity.objects.filter(account=a.id, civi__c_type="solution", activity_type__contains="pos")
        solution_threads = voted_solutions.distinct('thread__id').values_list('thread__id', flat=True)

        for thread_id in solution_threads:
            t = Thread.objects.get(id=thread_id)
            solutions = []
            solution_civis = voted_solutions.filter(thread=thread_id).values_list('civi__id', flat=True)
            for civi_id in solution_civis:
                c = Civi.objects.get(id=civi_id)
                vote = voted_solutions.get(civi__id=civi_id).activity_type
                vote_types = {
                    'vote_pos': 'Agree',
                    'vote_vpos': 'Strongly Agree'
                }
                solution_item = {
                    'id': c.id,
                    'title': c.title,
                    'body': c.body,
                    'user_vote': vote_types.get(vote)
                }
                solutions.append(solution_item)

            my_issue_item = {
                'thread_id': t.id,
                'thread_title': t.title,
                'category': t.category.name,
                'solutions': solutions
            }
            result['issues'].append(my_issue_item)

        result['representatives'] = []
        rep_ids = sun.get_legislator_ids_by_lat_long(a.latitude, a.longitude)

        for bio_id in rep_ids:
            rep = Representative.objects.get(bioguideID=bio_id)
            if rep:
                result['representatives'].append(rep.summarize())

        if request.user.username != user:
            ra = Account.objects.get(user=request.user)
            if user in ra.following.all():
                result['follow_state'] = True
            else:
                result['follow_state'] = False
        return JsonResponse(result)

    except Account.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))

def get_rep(request, rep_id):
    # TODO: FINISH THIS
    try:
        # Federal Representatives only
        u = Representative.objects.get(id=rep_id)
        a = Account.objects.get(user=u)
        result = Account.objects.summarize(a)

        result['representatives'] = []
        # result['issues'] = ['''{"category": "category", "issue":"Example Issue that the User probably cares about" }''']*20
        if request.user.username != user:
            ra = Account.objects.get(user=request.user)
            if user in ra.following.all():
                result['follow_state'] = True
            else:
                result['follow_state'] = False
        return JsonResponse(result)

    except Account.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))

def get_feed(request):
    try:
        a = Account.objects.get(user=request.user)
        all_categories = Category.objects.values_list('id', flat=True)
        user_categories = list(a.categories.values_list('id', flat=True)) or all_categories

        # feed_threads = [Thread.objects.summarize(t) for t in Thread.objects.filter_by_category(user_categories).order_by('-created')]
        # top5_threads = Thread.objects.all().order_by('-views')[:5].values('id', 'title')
        feed_threads = [Thread.objects.summarize(t) for t in Thread.objects.order_by('-created')]

        # data = {
        #     'threads': feed_threads,
        #     # 'trending_threads': top5_threads
        # }

        return json_response(feed_threads)

    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))

def get_thread(request, thread_id):
    try:
        t = Thread.objects.get(id=thread_id)
        civis = Civi.objects.filter(thread_id=thread_id)
        req_a = Account.objects.get(user=request.user)
        # problems = civis.filter(c_type='problem')
        # causes = civis.filter(c_type='cause')
        # solutions = civis.filter(c_type='solution')

        #TODO: move order by to frontend or accept optional arg
        c = civis.order_by('-created')
        c_scores = [ci.score(req_a.id) for ci in c]
        c_data = [Civi.objects.serialize_s(ci) for ci in c]
        for idx, item in enumerate(c_data):
            problems[idx]['score'] = c_scores[idx]
        problems = sorted(problems, key=lambda x: x['score'], reverse=True)
        # for idx, item in enumerate(problems):
        #     problems[idx] = json.dumps(item, cls=DjangoJSONEncoder)
        #
        # c = civis.filter(c_type='cause').order_by('-created')
        # c_scores = [ci.score(req_a.id) for ci in c]
        # causes = [Civi.objects.serialize_s(ci) for ci in c]
        # for idx, item in enumerate(causes):
        #     causes[idx]['score'] = c_scores[idx]
        # causes = sorted(causes, key=lambda x: x['score'], reverse=True)
        # for idx, item in enumerate(causes):
        #     causes[idx] = json.dumps(item, cls=DjangoJSONEncoder)
        #
        # c = civis.filter(c_type='solution').order_by('-created')
        # c_scores = [ci.score(req_a.id) for ci in c]
        # solutions = [Civi.objects.serialize_s(ci) for ci in c]
        # for idx, item in enumerate(solutions):
        #     solutions[idx]['score'] = c_scores[idx]
        # solutions = sorted(solutions, key=lambda x: x['score'], reverse=True)
        # for idx, item in enumerate(solutions):
        #     solutions[idx] = json.dumps(item, cls=DjangoJSONEncoder)

        # problems = [Civi.objects.serialize(c) for c in civis.filter(c_type='problem').order_by('-votes_vpos', '-votes_pos')]
        # problems =
        # causes = [Civi.objects.serialize(c) for c in civis.filter(c_type='cause').order_by('-votes_vpos', '-votes_pos')]
        # solutions = [Civi.objects.serialize(c) for c in civis.filter(c_type='solution').order_by('-votes_vpos', '-votes_pos')]

        data = {
            'title': t.title,
            'summary': t.summary,
            'hashtags': t.hashtags.all().values(),
            'author': {
                'username': t.author.user.username,
                'profile_image': t.author.profile_image.url  if t.author.profile_image  else "/media/profile/default.png",
                'first_name': t.author.first_name,
                'last_name': t.author.last_name
            },
            'category': model_to_dict(t.category),
            'created': t.created,
            # 'problems': problems,
            # 'causes': causes,
            # 'solutions': solutions,
            'contributors': [Account.objects.chip_summarize(a) for a in Account.objects.filter(pk__in=civis.distinct('author').values_list('author', flat=True))],
            'num_civis': t.num_civis,
            'num_views': t.num_views,
            'votes': [{'civi_id':act.civi.id, 'activity_type': act.activity_type, 'acct': act.account.id} for act in Activity.objects.filter(thread=t.id, account=req_a.id)]
        }

        #modify thread view count
        t.num_views = t.num_views + 1
        t.save()

        return json_response(data)
    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))

def get_civi(request, civi_id):
    try:
        c = Civi.objects.serialize(Civi.objects.get(id=civi_id))
        return JsonResponse(c, safe=False)
    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))

def get_civis(request, thread_id):
    try:
        c = [Civi.objects.serialize(c) for c in Civi.objects.filter(thread=thread_id)]
        return JsonResponse(c)
    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))


def get_responses(request, thread_id, civi_id):
    try:
        req_acct = Account.objects.get(user=request.user)
        c_qs = Civi.objects.get(id=civi_id).responses.all()
        c_scored = []
        for res_civi in c_qs:
            c_dict = res_civi.dict_with_score(req_acct.id)
            c_rebuttal = res_civi.responses.all()
            if c_rebuttal:
                c_dict['rebuttal'] = c_rebuttal[0].dict_with_score(req_acct.id)
            c_scored.append(c_dict)

        civis = sorted(c_scored, key=lambda c: c['score'], reverse=True)

        return JsonResponse(civis, safe=False)
    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))

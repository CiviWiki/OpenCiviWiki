import os, sys, json, pdb, random, hashlib
from models import Account, Topic, Attachment, Category, Civi, Comment, Hashtag, Group
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from utils.custom_decorators import require_post_params
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.db.models import Q

@login_required
@require_post_params(params=['title', 'description'])
def createGroup(request):
	'''
		USAGE:
			create a civi Group responsible for creating and managing civi content.
			Please validate file uploads as valid images on the frontend.

		File Uploads:
			profile (optional)
			cover (optional)

		Text POST:
			title
			description

		:returns: (200, ok, group_id) (500, error)
	'''
	pi = request.FILES.get('profile', False)
	ci = request.FILES.get('cover', False)
	title = request.POST.get(title, '')
	data = {
		"owner": Account.objects.get(user=request.user),
		"title": title,
		"description": request.POST.get('description',''),
		"profile_image": writeImage('profile', pi, title),
		"cover_image": writeImage('cover', ci, title)
	}

	try:
		group = Group(**data)
		group.save()
		account.groups.add(group)
		return JsonResponse({'result':group.id})
	except Exception as e:
		return HttpResponseServerError(reason=e)

@login_required
@require_post_params(params=['group', 'creator', 'topic', 'category', 'title', 'body', 'type'])
def createCivi(request):
	'''
	USAGE:
		use this function to insert a new connected civi into the database.

	Text POST:
		group
		creator
		topic
		category
		title
		body
		type
		reference (optional)
		at (optional)
		and_negative (optional)
		and_positive (optional)

	:return: (200, ok) (400, missing required parameter) (500, internal error)
	'''
	civi = Civi()
	data = {
		'group_id': request.POST.get('group', ''),
		'creator_id': request.POST.get('creator', ''),
		'topic_id': request.POST.get('topic', ''),
		'title': request.POST.get('title', ''),
		'body': request.POST.get('body', ''),
		'type': request.POST.get('type', ''),
		'visits': 0,
		'votes_neutral': 0,
		'votes_positive1': 0,
		'votes_positive2': 0,
		'votes_negative1': 0,
		'votes_negative2': 0,
		'reference_id': request.POST.get('reference', ''),
		'at_id': request.POST.get('at', ''),
		'and_negative_id': request.POST.get('and_negative', ''),
		'and_positive_id': request.POST.get('and_positive', ''),
	}
	try:
		civi = Civi(**data)

		hashtags = request.POST.get('hashtags', '')
		split = [x.strip() for x in hashtags.split(',')]
		for str in split:
			if not Hashtag.objects.filter(title=str).exists():
				hash = Hashtag(title=str)
				hash.save()
			else:
				hash = Hashtag.objects.get(title=str)

			civi.hashtags.add(hash.id)
		civi.save()
		return HttpResponse()
	except Exception as e:
		return HttpResponseServerError(reason=str(e))

@login_required
def editUser(request):
	'''

	USAGE:
		Use this function to update any of a users attributes, all fields are optional.
		Please validate file uploads as valid images on the frontend.

		THESE ATTRIBUTES CANNOT BE EDITED BY THIS METHOD:
			-statistics -pins -history -friends -awards

		File Uploads:
			profile (image)
			cover (image)

		Text POST:
		 	first_name
			last_name
			email
			about_me
			interests
			address1
			address2
			city
			state
			country
			zip_code

	:return: (200, ok) (500, error)

	'''
	r = json.loads(dict(request.POST)['data'][0])
	user = request.user
	account = Account.objects.get(user=user)
	interests = r.get('interests', False)
	if interests:
		interests = list(interests)
	else:
		interests = account.interests



	profile_image = account.profile_image
	cover_image = account.cover_image
	pi = request.FILES.get('profile', False)
	ci = request.FILES.get('cover', False)
	if pi:
		url = "{media}{type}/{username}.png".format(media=settings.MEDIA_ROOT_URL, type='profile',username=account.user.username)
		with open( url , 'wb+') as destination:
			for chunk in pi.chunks():
				destination.write(chunk)
		profile_image = "{media}{type}/{username}.png".format(media=settings.MEDIA_ROOT_URL, type='profile',username=account.user.username)
	else:
		profile_image = "{media}{type}/{username}.png".format(media=settings.MEDIA_ROOT_URL, type='profile',username='generic')


	if ci:
		url = "{media}{type}/{username}.png".format(media=settings.MEDIA_ROOT_URL, type='cover',username=account.user.username)
		with open( url , 'wb+') as destination:
			for chunk in ci.chunks():
				destination.write(chunk)

		cover_image = "{media}{type}/{username}.png".format(media=settings.MEDIA_ROOT_URL, type='cover',username=account.user.username)
	else:
		cover_image = "{media}{type}/{username}.png".format(media=settings.MEDIA_ROOT_URL, type='cover',username='generic')

	data = {
		"first_name":r.get('first_name', account.first_name),
		"last_name":r.get('last_name', account.last_name),
		"email":r.get('email', account.email),
		"about_me":r.get('about_me', account.about_me),
		"interests": interests,
		"profile_image":profile_image,
		"cover_image":cover_image,
		"address1": r.get('address1', account.address1),
		"address2": r.get('address2', account.address2),
		"city": r.get('city', account.city),
		"state": r.get('state', account.state),
		"zip_code": r.get('zip_code', account.zip_code),
		"country": r.get('country', account.country)
	}

	try:
		Account.objects.filter(id=account.id).update(**data)
		account.refresh_from_db()

		return JsonResponse({"result":Account.objects.serialize(account)})
	except Exception as e:
		return HttpResponseServerError(reason=str(e))

@login_required
@require_post_params(params=['friend'])
def requestFriend(request):
	'''
		USAGE:
			Takes in a user_id and sends your id to the users friend_requests list. No join
			is made on accounts until user accepts friend request on other end.

		Text POST:
			friend

		:return: (200, okay) (400, error) (500, error)
	'''
	try:
		account = Account.objects.get(user=request.user)
		friend = Account.objects.get(id=request.POST.get('friend', -1))
		if account.id in friend.friend_requests:
			raise Exception("Request has already been sent to user")

		friend.friend_requests += [int(account.id)]
		friend.save()
		return HttpResponse()
	except Account.DoesNotExist as e:
		return HttpResponseBadRequest(reason=str(e))
	except Exception as e:
		return HttpResponseServerError(reason=str(e))

@login_required
@require_post_params(params=['friend'])
def acceptFriend(request):
	'''
		USAGE:
			Takes in user_id from current friend_requests list and joins accounts as friends.
			Does not join accounts as friends unless the POST friend is a valid member of the friend request array.

		Text POST:
			friend

		:return: (200, okay, list of friend information) (400, bad lookup) (500, error)
	'''
	try:
		account = Account.objects.get(user=request.user)
		stranger = Account.objects.get(id=request.POST.get('friend', -1))

		if stranger_id not in account.friend_requests:
			raise Exception(reason="No request was sent from this person.")

		account.friend_requests = [fr for fr in account.friend_requests if fr != stranger_id]
		account.friends.add(stranger)
		account.save()
		return JsonResponse({"result":Account.objects.serialize(account, "friends")})
	except Account.DoesNotExist as e:
		return HttpResponseBadRequest(reason=str(e))
	except Exception as e:
		return HttpResponseServerError(reason=str(e))

@login_required
@require_post_params(params=['friend'])
def rejectFriend(request):
	'''
		USAGE:
			Takes in user_id from current friend_requests list and removes it.

		Text POST:
			friend

		:return: (200, okay, list of friend information) (400, bad lookup) (500, error)
	'''
	try:
		account = Account.objects.get(user=request.user)
		stranger = Account.objects.get(id=request.POST.get('friend', -1))

		if stranger.id not in account.friend_requests:
			raise Exception("No request was sent from this person.")

		account.friend_requests = [fr for fr in account.friend_requests if fr != stranger_id]
		account.save()

		return JsonResponse({"result":Account.objects.serialize(account, "friends")})
	except Account.DoesNotExist as e:
		return HttpResponseBadRequest(reason=str(e))
	except Exception as e:
		return HttpResponseServerError(reason=str(e))

@login_required
@require_post_params(params=['friend'])
def removeFriend(request):
	'''
		USAGE:
			takes in user_id from current friends and removes the join on accounts.

		Text POST:
			friend

		:return: (200, okay, list of friend information) (500, error)
	'''
	account = Account.objects.get(user=request.user)
	try:
		friend = Account.objects.get(id=request.POST.get('friend', -1))
		account.friends.remove(friend)
		account.save()
		return JsonResponse(Account.objects.serialize(account, "friends"))
	except Account.DoesNotExist as e:
		return HttpResponseServerError(reason=str(e))

@login_required
@require_post_params(params=['group'])
def followGroup(request):
	'''
		USAGE:
			given a group ID number, add user as follower of that group.

		Text POST:
			group

		:return: (200, ok, list of group information) (400, bad request) (500, error)
	'''

	account = Account.objects.get(user=request.user)
	try:
		group = Group.objects.get(id=request.POST.get('group', -1))
		account.group.add(group)
		account.save()
		return JsonResponse({"result":Account.objects.serialize(account, "groups")}, safe=False)
	except Group.DoesNotExist as e:
		return HttpResponseBadRequest(reason=str(e))
	except Exception as e:
		return HttpResponseServerError(reason=str(e))

@login_required
@require_post_params(params=['group'])
def unfollowGroup(request):
	'''
		USAGE:
			given a group ID numer, remove user as a follower of that group.

		Text POST:
			group

		:return: (200, ok, list of group information) (400, bad request) (500, error)
	'''

	account = Account.objects.get(user=request.user)
	try:
		group = Group.objects.get(id=request.POST.get('group', -1))
		account.group.remove(group)
		return JsonResponse({"result":Account.objects.serialize(account, "group")}, safe=False)
	except Group.DoesNotExist as e:
		return HttpResponseBadRequest(reason=str(e))
	except Exception as e:
		return HttpResponseServerError(reason=str(e))


@login_required
@require_post_params(params=['civi'])
def pinCivi(request):
	'''
		USAGE:
			given a civi ID numer, pin the civi.

		Text POST:
			civi

		:return: (200, ok, list of pinned civis) (400, bad request) (500, error)
	'''

	account = Account.objects.get(user=request.user)
	try:
		civi = Civi.objects.get(id=request.POST.get('civi', -1))
		if civi.id not in account.pinned:
			account.pinned += civi.id
			account.save()
		return JsonResponse({"result":Account.objects.serialize(account, "group")}, safe=False)

	except Civi.DoesNotExist as e:
		return HttpResponseBadRequest(reason=str(e))
	except Exception as e:
		return HttpResponseServerError(reson=str(e))



@login_required
@require_post_params(params=['id'])
def unpinCivi(request):
	'''
		USAGE:
			given a civi ID numer, unpin the civi.

		Text POST:
			civi

		:return: (200, ok, list of pinned civis) (400, bad request) (500, error)
	'''
	account = Account.objects.get(user=request.user)
	try:
		cid = Civi.objects.get(id=request.POST.get("id", -1))
		if cid in account.pinned:
			account.pinned = [e for e in account.pinned if e != cid]
			account.save()

		return JsonResponse({"result":Account.objects.serialize(account, "group")}, safe=False)
	except Civi.DoesNotExist as e:
		return HttpResponseBadRequest(reason=str(e))
	except Exception as e:
		return HttpResponseServerError(reason=str(e))

def writeImage(type, img,  title):
	if img:
		url = "{media}{type}/{title}.png".format(media=settings.MEDIA_ROOT_URL, type=type,title=title)
		with open( url , 'wb+') as destination:
			for chunk in img.chunks():
				destination.write(chunk)
		return url
	else:
		return "{media}{type}/{title}.png".format(media=settings.MEDIA_ROOT_URL, type=type,title='generic')

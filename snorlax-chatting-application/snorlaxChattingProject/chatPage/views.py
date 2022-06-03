from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import json
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from .models import Chat, Contact
from django.http import JsonResponse
# Create your views here.

User = get_user_model()


@login_required
def home(request, chatID):
    # renders the homepage with a chat open
    return render(request, "chatPage/mainPage.html", {
        "chatID_json": mark_safe(json.dumps(chatID)),
        "username": mark_safe(json.dumps(request.user.username)),
        "contact_list": get_user_contact(request.user.username),
        "chat_list": get_chat_list(request.user.username),
        "current_user": request.user,
        "current_chat": get_current_chat(chatID),
    })


@login_required
def homepage(request):
    # renders the homepage without any chat open
    return render(request, "chatPage/mainPage.html", {
        "chatID_json": "null",
        "username": mark_safe(json.dumps(request.user.username)),
        "contact_list": get_user_contact(request.user.username),
        "chat_list": get_chat_list(request.user.username),
        "current_user": request.user,
        "current_chat": None,
    })


def get_last_10_messages(chatID):
    # gets the last 10 messages of a specific chat
    chat = get_object_or_404(Chat, id=chatID)
    return chat.chat_messages.order_by('timestamp').all()[:10]


def get_user_contact(username):
    # returns the friend list of the user
    # wrote this function so that I can use it to expand the project to contain
    # a accept and reject message condition in the case the user sends a
    # message to some the user never sent a message before
    # Case (might implement): Suppose User A never sent a message to User B. So
    # if User A searches for User B and sends him a message User B will have
    # the option to accept or reject the message. If User B accepts the message
    # then a chat will be created else User can not send a chat to User B for a
    # certain amount of time

    user = get_object_or_404(User, username=username)
    contact = Contact.objects.get(owner=user)

    friend_list = contact.friends.all()
    return friend_list


def get_chat_list(username):
    # returns the chat list of the user
    chat_list = Chat.objects.filter(participants__username__iexact=username)

    return chat_list


def get_author(username):
    # returns the author
    return get_object_or_404(User, username=username)


def get_current_chat(chatID):
    # returns the current chat
    return get_object_or_404(Chat, id=chatID)


def search_result(request):
    # returns the live search result
    if (request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        contact_name = request.POST.get('contact_name')
        other_users = User.objects.filter(username__icontains=contact_name)
        if len(other_users) > 0 and len(contact_name) > 0:
            data = []
            for user in other_users:
                if user.username != request.user.username:
                    indiv_user = {
                        'name': user.username,
                        "url": reverse('chatPage:chatSearch', kwargs={"chat_user_name": user.username})
                    }
                    data.append(indiv_user)
            res = data
        else:
            res = None

        return JsonResponse({'data': res})
    return JsonResponse({})


def chat_from_search(request, chat_user_name):
    # creates or opens a chat from the search bar result
    participant = get_object_or_404(User, username=chat_user_name)
    current_user = get_object_or_404(User, username=request.user.username)
    current_user_username = request.user.username
    personalContactBookExist = Contact.objects.filter(owner__username__iexact=current_user_username)
    otherContactBookExist = Contact.objects.filter(owner__username__iexact=chat_user_name)
    chatExist = Chat.objects.filter(participants__username__iexact=current_user_username)
    chatExist = chatExist.filter(participants__username__iexact=chat_user_name)
    if (not personalContactBookExist):
        # create a contact for personal use
        personalContactBook = Contact.objects.create(
            owner=current_user,
        )
        personalContactBook.save()
    else:
        # personal contact book exists
        personalContactBook = personalContactBookExist[0]

    # add the other person as a friend if not exist if exist as a friend
    if (participant not in personalContactBook.friends.all()):
        personalContactBook.friends.add(participant)
        personalContactBook.save()

    if (not otherContactBookExist):
        # create a contact for the other person
        otherContactBook = Contact.objects.create(
            owner=participant,
        )
        otherContactBook.save()
    else:
        otherContactBook = otherContactBookExist[0]

    # add the other person as a friend if not exist if exist as a friend
    if (current_user not in otherContactBook.friends.all()):
        otherContactBook.friends.add(current_user)
        otherContactBook.save()

    # get chat id
    if (chatExist):

        chatID = chatExist[0].id
    else:
        # create a chat with these participants and assign the chat id
        new_chat = Chat.objects.create()
        new_chat.participants.add(current_user)
        new_chat.participants.add(participant)
        new_chat.save()
        chatID = new_chat.id

    return render(request, "chatPage/mainPage.html", {
        "chatID_json": mark_safe(json.dumps(chatID)),
        "username": mark_safe(json.dumps(request.user.username)),
        "contact_list": get_user_contact(request.user.username),
        "chat_list": get_chat_list(request.user.username),
        "current_user": request.user,
        "current_chat": get_current_chat(chatID),
    })

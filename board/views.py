import datetime
from operator import itemgetter
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Template, Context, RequestContext
from django.contrib.auth.models import User, Group
from django.utils import simplejson
from board.models import *


def is_admin(user):
    if user:
        if user.groups.filter(name='admins').count() == 1:
            return True
        else:
            return False
    else:
        return False

def is_board(user):
    if user:
        if user.groups.filter(name='boarj').count() == 1:
            return True
        else:
            return False
    else:
        return False

def home(request):
    if request.is_ajax():
        slug = request.POST["slug"]
        #Check if slug can make a valid URL
        validchars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_~'
        returnstring = 'valid'
        for character in slug:
            if character not in validchars:
                returnstring = 'invalid'
                break
        # If it is a valid URL, check if it exists already
        if returnstring == 'valid':
            existing_boards = Board.objects.filter(slug=slug)
            existing_users = User.objects.filter(username=slug)
            if len(existing_boards) == 0 and len(existing_users) == 0:
                returnstring = 'available'
            else:
                returnstring = 'taken'
        print returnstring
        return HttpResponse(returnstring)
    if request.method == 'POST':
        if 'new_slug' in request.POST:
            # Set up user for the board to allow access (username and slug are identical)
            slug = request.POST['new_slug']
            slug = slug.lower()
            password = request.POST['password']
            email = request.user.email
            new_user = User.objects.create_user(slug, email, password) 
            board_group = Group.objects.get(name = 'boards')
            board_group.user_set.add(new_user)
            board_group.save()
            title = request.POST['title']
            # Create datetime objects from the different fields
            opening_date_list = request.POST['opening_date'].split("/") # Date is in British format: dd/mm/yyyy
            opening_date = datetime.date(int(opening_date_list[2]), int(opening_date_list[1]), int(opening_date_list[0]))
            opening_time_list = request.POST['opening_time'].split(":") # Time is in hh:mm - 24 h format
            opening_time = datetime.time(int(opening_time_list[0]), int(opening_time_list[1]))
            opening = datetime.datetime.combine(opening_date, opening_time)
            closing_date_list = request.POST['closing_date'].split("/") # Date is in British format: dd/mm/yyyy
            closing_date = datetime.date(int(closing_date_list[2]), int(closing_date_list[1]), int(closing_date_list[0]))
            closing_time_list = request.POST['closing_time'].split(":") # Time is in hh:mm - 24 h format
            closing_time = datetime.time(int(closing_time_list[0]), int(closing_time_list[1]))
            closing = datetime.datetime.combine(closing_date, closing_time)
            new_board = Board(
                    title = title, slug = slug, open_for = new_user,
                    admin = request.user, opening = opening,
                    closing = closing)
            new_board.save()
            return HttpResponseRedirect(new_board.get_absolute_url())
    return render_to_response('home.html',
            {},
            context_instance = RequestContext(request)
        )

def show_board(request, slug):
    board = Board.objects.get(slug = slug)
    messages = Message.objects.filter(belongs_to = board)
    if request.is_ajax():
        message_list = []
        for message in messages:
            voted = False
            if 'voted' in request.session:
                print request.session.get('voted')
                if str(message.id) in request.session.get('voted'):
                    voted = True
            tpl = (message.votes, message.post_date, message.text, voted, str(message.id))
            message_list.append(tpl)
        sorted_list = sorted(message_list, key=itemgetter(1,2))
        list_without_dates = []
        for message in sorted_list:
            message_without_date = (message[0], message[2], message[3], message[4]) #Somehow python date and json don't play.
            list_without_dates.append(message_without_date)
        json = simplejson.dumps(list_without_dates)
        return HttpResponse(json, mimetype='application/json')
    if request.method == 'POST':
        text = request.POST['comment']
        message = Message(
                text = text,
                belongs_to = board,
                post_date = datetime.datetime.now(),
                votes = 0
            )
        message.save()
    return render_to_response('board.html',
            {'board': board, 'messages': messages, 'autorefresh': True},
            context_instance = RequestContext(request)
        )

def vote_up(request, comment_id):
    variable_exists = False
    comment = Message.objects.get(id = comment_id)
    board = comment.belongs_to
    if 'voted' in request.session:
        variable_exists = True
        voted = request.session.get('voted')
        if comment_id in voted:
            return HttpResponseRedirect(board.get_absolute_url())
    comment.votes += 1
    comment.save()
    if variable_exists:
        voted.append(comment_id)
    else:
        voted = [comment_id,]
    request.session['voted'] = voted
    return HttpResponseRedirect(board.get_absolute_url())

def vote_down(request, comment_id):
    variable_exists = False
    comment = Message.objects.get(id = comment_id)
    board = comment.belongs_to
    if 'voted' in request.session:
        variable_exists = True
        voted = request.session.get('voted')
        if comment_id in voted:
            return HttpResponseRedirect(board.get_absolute_url())
    comment.votes -= 1
    comment.save()
    if variable_exists:
        voted.append(comment_id)
    else:
        voted = [comment_id,]
    request.session['voted'] = voted
    return HttpResponseRedirect(board.get_absolute_url())

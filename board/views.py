import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Template, Context, RequestContext
from board.models import *
#from board.forms import *

def home(request):
    board = Board.objects.get(slug = 'eu_1')
    messages = Message.objects.filter(belong_to = board)
    return render_to_response('board.html',
            {'board': board, 'messages': messages}
        )

def set_up_board(request):
    if request.method == 'POST':
        pass
    else:
        form = set_up_form()
    return render_to_response('set_up_board.html',
            {}
        )

def show_board(request, slug):
    board = Board.objects.get(slug = slug)
    messages = Message.objects.filter(belong_to = board)
    if request.method == 'POST':
        text = request.POST['comment']
        message = Message(
                message = text,
                belong_to = board,
                post_date = datetime.datetime.now(),
                votes = 0
            )
        message.save()
    return render_to_response('board.html',
            {'board': board, 'messages': messages},
            context_instance = RequestContext(request)
        )

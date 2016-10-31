import operator
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render, render_to_response,redirect
from django.http import *
from django.urls import reverse
from django.template import loader, RequestContext
from django.contrib import messages
from .models import Question, Search, MyUser
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from polls.forms import *
from django.views.decorators.csrf import csrf_exempt


def login(request):
    email = password = ''
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']

        user = MyUser.objects.get(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/polls/')
    return render_to_response('polls/registration/login.html', context_instance=RequestContext(request))

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            u = MyUser()
            user = u.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], date_of_birth=form.cleaned_data['date_of_birth'])
            user.set_password(self.cleaned_data["password1"])
            user.save()
            return HttpResponseRedirect('/polls/')
    form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('polls/registration/signup.html',variables)

def index(request):
    recent_q = Question.objects.filter(pub_date__range=(datetime.now()
        - timedelta(hours=48),datetime.now())).order_by('-pub_date')
    questioned = Question.objects.order_by('-pub_date')[recent_q.count():15]
    context = {'questioned': questioned,
                'recent_q': recent_q}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    # Same as the Try & Except
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        selected_choice.votes += 1
        selected_choice.save()
    except:
        return render(request, 'polls/detail.html', {
        'question': question,
        'error_message': "No choice was selected.",
        })

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def search_results(request):
    query = request.GET['q']
    t = loader.get_template('polls/search_results.html')
    questioned = Question.objects.filter(question_text__icontains=query)
    if query in [None, '']:
        m = messages.add_message(request, messages.ERROR, "Can't search empty strings.")
        return HttpResponse(t.render(m))
    else:
        search = Search.objects.create(search_text = query, pub_date = datetime.now())
        search.save()
        most = Search.most_common("search_text")
        context = { 'questioned': questioned, 'most': most }
        return HttpResponse(t.render(context))

import operator
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader
from .models import Question, Search
from django.db.models import Q


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
    search = Search.objects.create(search_text = query, pub_date = datetime.now())
    search.save()
    context = { 'questioned': questioned }
    return HttpResponse(t.render(context))

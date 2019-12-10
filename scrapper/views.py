from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
import requests
from bs4 import BeautifulSoup

from .models import Choice, Question
from django.urls import reverse
from django.views import generic


def get_html(url):
    """
    Returns HTML page code
    """
    r = requests.get(url)
    return r.text


def get_main_data(html):
    """
    Get main data about page.
    This function returns next data:
        *   h1
        *   Title
        *   Description
    """
    soup = BeautifulSoup(html, 'lxml')
    h1 = soup.find('div', class_='catalog-masthead').find('h1', class_='catalog-masthead__title').text
    h1_result = h1.strip()
    return h1_result


# All functions without HTML code output are above this comment.

def home_page(request):
    return render(request, 'scrapper/home.html')


def scrap_home(request):
    """
    Main scrapper page.
    Functions:
        *   Input URL - get main data in the next page
    """
    # url = 'https://catalog.onliner.by/mobile/apple/iphone732'
    # result_data = get_main_data(get_html(url))
    return render(request, 'scrapper/scrap_home.html')

def scrap_result(request):
    """
    Page about results scrapping.
    In this page we can:
        *   Save results in DB
        *   Download resusts in CSV
    """
    url = request.POST['url']
    result_data = get_main_data(get_html(url))
    return render(request, 'scrapper/scrap_result.html', {'result_data': result_data})


def reports_list(request):
    """
    What doing this Function?
    """
    return render(request, 'scrapper/reports.html')


def scrapper_set(request):
    """
    What doing this Function?
    """
    return render(request, 'scrapper/scrap_set.html')


# TEST Views
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'scrapper/polls/index.html', context)
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'scrapper/polls/detail.html', {'question': question})
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'scrapper/polls/results.html', {'question': question})
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 'scrapper/polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         return HttpResponseRedirect(reverse('results', args=(question.id,)))


class IndexView(generic.ListView):
    template_name = 'scrapper/polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'scrapper/polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'scrapper/polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'scrapper/polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('results', args=(question.id,)))
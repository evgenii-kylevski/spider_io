from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
import requests, csv
from random import choice
from bs4 import BeautifulSoup
from .models import Session
from django.utils import timezone


def get_proxy():
    html = requests.get('https://free-proxy-list.net/').text
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find('table', id='proxylisttable').find_all('tr')[1:11]

    proxies = []

    for tr in trs:
        tds = tr.find_all('td')
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
        proxy = {'schema': schema, 'address': ip + ':' + port}
        proxies.append(proxy)

    return choice(proxies)


def get_html(url):
    """
    Returns HTML page code
    """
    p = get_proxy()
    proxy = {p['schema']: p['address']}
    r = requests.get(url, proxies=proxy, timeout=5)
    r = requests.get(url)
    return r.text


def write_csv(data_set):
    with open('scrapper/data/dataset.csv', 'a') as file_csv:
        writer = csv.writer(file_csv)

        writer.writerow((
            data_set['url'],
            data_set['h1'],
            data_set['title']
        ))


def down_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dataset.csv"'

    return response


def get_main_data(html, url):
    """
    Get main data about page.
    This function returns next data:
        *   h1
        *   Title
    """
    soup = BeautifulSoup(html, 'lxml')

    h1 = soup.find('div', class_='catalog-masthead').find('h1', class_='catalog-masthead__title').text.strip()
    title = soup.find('head').find('title').text.strip()

    data_set = {'h1': h1,
                'title': title,
                'url': url}

    return data_set


def record_session(result_data):
    # sessions = Session.object.all()

    record_session = Session(
        h1=result_data['h1'],
        title=result_data['title'],
        url=result_data['url'],
        scrapping_time=timezone.now()
    )
    record_session.save()


# All functions without HTML code output are above this comment.

def home_page(request):
    return render(request, 'scrapper/home.html')


def scrap_home(request):
    """
    Main scrapper page.
    Functions:
        *   Input URL - get main data in the next page
    """
    return render(request, 'scrapper/scrap_home.html')


def scrap_result(request):
    """
    Page about results scrapping.
    In this page we can:
        *   Save results in db
        *   Download results in CSV
    """

    # To check if multiple URLs are entered
    # urls = request.POST['url']
    # result_data_dict = {}
    # if urls.find('\r\n'):
    #     urls = urls.split('\r\n')
    #     for url in urls:
    #         if url:
    #             result_data = get_main_data(get_html(url))
    #             result_data.update({'url': request.POST['url']})
    #             result_data.update({'url': url})
    #
    #             if request.POST['save_csv']:
    #                 write_csv(result_data)

    url = request.POST['url']
    result_data = get_main_data(get_html(url), url)

    # If you want to download CSV file
    if request.POST['save_csv']:
        write_csv(result_data)

    # Save data in db
    record_session(result_data)

    return render(request, 'scrapper/scrap_result.html', result_data)


def reports_list(request):
    """
    What doing this Function?
    """
    sessions = Session.pubs.all()
    return render(request, 'scrapper/reports.html', {'sessions': sessions})

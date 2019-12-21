from .models import MobileProduct, CatalogMobile
from bs4 import BeautifulSoup
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from pyvirtualdisplay import Display
from random import choice
from selenium import webdriver
from slugify import slugify
import csv
import os
import requests
import time


chromedriver = '../spider-io-django/bin/chromedriver'
os.environ["webdriver.chrome.driver"] = chromedriver
display = Display(visible=0, size=(800, 600))
display.start()


class OnlinerBot:

    def __init__(self):

        self.driver = webdriver.Chrome(chromedriver)
        self.total_products = []
        self.exception_words = ['Смартфон', '(белый)', '(синий)', '(красный)', '(черный)', '(зеленый)', '(розовый)',
                                '(золотисный)', '(серебристый)', 'Dual', 'SIM', '(оранжевый)', '(фиолетовый)',
                                '(Мобильный)', '(телефон)', '(голубой)', '(лавандовый)', '(ультрафиолет)',
                                'Black', 'Gold', 'Blue', 'Pink', 'Apricot', 'Rose', 'Pearl', 'White',
                                '(2019)', '(2018)', '(2017)', '(2016)', '(2015)', 'китайская', '(золото)',
                                'Single', 'Gray', 'Silver', 'Sapphire', '(ультрафиолет)',
                                'международная', 'версия', '(матовый', 'синий)', '(синий', 'изумруд)', 'черный)',
                                '(золотистый)', '(золотист.)', '(прозрачный', 'титан)', '(сумеречное', 'золото)',
                                'индийская', 'Fashion', 'Classic', 'Grey', 'Purple', 'золото)', 'Special',
                                'Edition', 'Fashion', 'Classic', 'Grey', 'Purple', 'золото)', '(PRODUCT)RED™',
                                '(темно-зеленый)', '(серый', 'космос)', 'Space', 'Grey', 'Purple', 'золото)',
                                '(коралловый)', '(серый)', '(розовое', '(PRODUCT)RED™', '(перламутр)',
                                '(оникс)', '(аквамарин)', '(гранат)', '(цитрус)', '(желтый)', '(черный',
                                'бриллиант)', '(арктический', '(титан)', '(аура)', '(серая', 'орхидея)',
                                'сапфир)', '(белая', '(медный)', '(королевский', 'рубин)', '(королевский',
                                'рубин)', '(мистический', 'аметист)', '(коралловый', '(цветущий', 'розовый)',
                                'Olympic', 'Games', 'Limited', 'Мобильный', 'телефон', 'Cyan',
                                '(глянцевый', 'индиго)', 'белый)', '(бирюзовый)', '(стальной)', '(индиго)',
                                '(железо/сталь)', '(индиго/серебристый)', '(железо/сталь)', '(сталь/медь)',
                                '(темно-серый)', '(индиго)', '(стальной)', '(синий/серебристый)', '(синий/медный)',
                                '(лимитированная', 'серия)', '(песочный)', '(легендарная', 'модель)']

    def check_db(self):
        pass

    def get_selenium_objects(self, brand_name):

        product_names_set = set()
        page = 1

        while True:
            url = "https://catalog.onliner.by/mobile?mfr%5B0%5D={}&page={}".format(brand_name, str(page))

            self.driver.get(url)
            time.sleep(5)

            # items = self.driver.find_elements_by_class_name("schema-product__title")
            items = self.driver.find_elements_by_class_name("schema-product__part_2")
            time.sleep(2)

            if len(items) == 0:
                break

            for item in items:
                try:
                    div_block = item.find_element_by_class_name("schema-product__title")
                    name_list = div_block.find_element_by_tag_name('span').text.split()
                    product_name = ' '.join((item for item in name_list if item not in self.exception_words))
                except:
                    product_name = ""

                try:
                    product_url = item.find_element_by_tag_name('a').get_attribute('href')
                except:
                    product_url = ""

                try:
                    div_block = item.find_element_by_class_name("schema-product__line")
                    product_price = int(div_block.find_element_by_tag_name('span').text.split()[0].split(',')[0])
                except:
                    product_price = ""

                if product_name and product_url:
                    product_slug = slugify(product_name)
                    new_product = [product_name, product_url, product_price, product_slug]

                    if product_name not in product_names_set:
                        product_names_set.add(product_name)
                        self.total_products.append(new_product)

            page += 1

        self.driver.close()
        return self.total_products

    def get_BS_objects(self):
        pass

    def update_DB(self):
        pass

    def download_csv(self):
        self.response = HttpResponse(content_type='text/csv')
        self.response['Content-Disposition'] = 'attachment; filename="dataset.csv"'

        for el in self.total_products:
            writer = csv.writer(self.response)
            writer.writerow(el)

        return self.response


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
    # p = get_proxy()
    # proxy = {p['schema']: p['address']}
    # r = requests.get(url, proxies=proxy, timeout=5)
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


def down_csv():
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dataset.csv"'

    return response


def get_product_mobile_data(html):
    soup = BeautifulSoup(html, 'lxml')
    products_list1 = soup.find_all('div', class_="offers-description__info")
    # products_list2 = products_list1.find_all('div', class_="schema-product__group")
    for product in products_list:
        brand_name = soup.find('div', class_="schema-tags__item").find('div', class_="schema-tags__item").find('span').text
        not_full_product_info = product.find('div', class_="schema-product__part schema-product__part_2")
        not_full_product_name = not_full_product_info.find('div', class_="schema-product__part schema-product__part_4").find('div', class_="schema-product__title")
        product_name = not_full_product_name.find('a').find('span').text
        # product_description = # TextField
        # product_rating = # IntegerField
        # product_review = # URLField
        # product_price = # FloatField
        product_url = not_full_product_name.find('a').get('href')
    pass


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
    return render(request, 'scrapper/scrap_home.html')

def scrap_result(request):

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

    if request.POST['brand_name']:
        brand_name = request.POST['brand_name']
        new_session = OnlinerBot()
        new_session.get_selenium_objects(request.POST['brand_name'])
        # if request.POST['save_csv']:
        #     new_session.download_csv()
        return render(request,
                      'scrapper/scrap_result.html',
                      {'brand_name': brand_name, 'total_products': new_session.total_products})


def reports_list(request):
    return render(request, 'scrapper/reports.html')


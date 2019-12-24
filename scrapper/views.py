from .models import MobileProduct, CatalogMobile
from bs4 import BeautifulSoup
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from pyvirtualdisplay import Display
from random import choice
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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
        self.exception_words = [
            'Смартфон', '(белый)', '(синий)', '(красный)', '(черный)', '(зеленый)', '(розовый)',
            '(золотисный)', '(серебристый)', 'Dual', 'SIM', '(оранжевый)', '(фиолетовый)',
            '(Мобильный)', '(телефон)', '(голубой)', '(лавандовый)', '(ультрафиолет)',
            'Black', 'Gold', 'Blue', 'Pink', 'Apricot', 'Rose', 'Pearl', 'White',
            '(2019)', '(2018)', '(2017)', '(2016)', '(2015)', 'китайская', '(золото)',
            'Single', 'Gray', 'Silver', 'Sapphire', '(ультрафиолет)', '(грифельно-синий)',
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
            'Olympic', 'Games', 'Limited', 'Мобильный', 'телефон', 'Cyan', '(бронзовый)',
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

            items = self.driver.find_elements_by_class_name("schema-product__part_2")
            time.sleep(2)

            if len(items) == 0:
                break

            for item in items:
                try:
                    div_block_title = item.find_element_by_class_name("schema-product__title")
                    name_list = div_block_title.find_element_by_tag_name('span').text.split()
                    product_name = ' '.join((item for item in name_list if item not in self.exception_words))
                except NameError:
                    product_name = ""

                try:
                    div_block_title = item.find_element_by_class_name("schema-product__title")
                    brand_url = div_block_title.find_element_by_tag_name('a').get_attribute('href')
                except NameError:
                    brand_url = ""

                try:
                    div_block_line = item.find_element_by_class_name("schema-product__line")
                    product_price = int(div_block_line.find_element_by_tag_name('span').text.split()[0].split(',')[0])
                except NoSuchElementException:
                    product_price = 0

                if product_name and brand_url:
                    product_slug = slugify(product_name)
                    scrapping_time = timezone.now()
                    new_product = [product_name, brand_url, product_slug, product_price, scrapping_time]
                    if product_name not in product_names_set:
                        product_names_set.add(product_name)
                        self.total_products.append(new_product)

            page += 1

        self.driver.close()
        return self.total_products

    def update_db(self, brand_name):
        for product in self.total_products:
            settings = 'need to update'
            try:
                product_in_db = CatalogMobile.objects.get(product_slug=product[2])
                if product_in_db:
                    product_in_db.brand_name = brand_name
                    product_in_db.product_name = product[0]
                    product_in_db.brand_url = product[1]
                    product_in_db.product_slug = product[2]
                    product_in_db.product_price = product[3]
                    product_in_db.scrapping_time = product[4]
                    product_in_db.save()
                settings = 'updated'
            except Exception as DoesNotExist:
                pass

            if settings != 'updated':
                new_record = CatalogMobile.objects.create(
                    brand_name=brand_name,
                    product_name=product[0],
                    brand_url=product[1],
                    product_slug=product[2],
                    product_price=product[3],
                    scrapping_time=product[4]
                )
                new_record.save()

    def download_csv(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="dataset.csv"'

        for el in self.total_products:
            writer = csv.writer(response)
            writer.writerow(el)

        return response


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

def find_all_brand_names():
    obj = CatalogMobile.objects.order_by('brand_name').all()
    brand_names_list = []
    for elem in obj:
        if elem.brand_name not in brand_names_list:
            brand_names_list.append(elem.brand_name)
    return brand_names_list


# All functions without HTML code output are above this comment.


def home_page(request):
    return render(request, 'scrapper/home.html')


def scrap_home(request):
    brand_names_list = find_all_brand_names()
    return render(request, 'scrapper/scrap_home.html', {'brand_names_list': brand_names_list})


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
        new_session.update_db(request.POST['brand_name'])
        # if request.POST['save_csv']:
        #     new_session.download_csv()
        return render(request,
                      'scrapper/scrap_result.html',
                      {'brand_name': brand_name, 'total_products': new_session.total_products})


def reports_list(request, brand_name='default', order_by='default', search_field='default'):
    options_to_display = {'brand_name': 'apple', 'order_by': '-product_price'}
    brand_names_list = find_all_brand_names()
    total_products = []

    # Setting for filters
    try:
        if request.POST['brand_name'] != 'default':
            options_to_display.update([('brand_name', request.POST['brand_name'])])
        if request.POST['order_by'] != 'default':
            options_to_display.update([('order_by', request.POST['order_by'])])
        tp_from_bd = CatalogMobile.objects.filter(brand_name=options_to_display['brand_name']).order_by(options_to_display['order_by']).all()
        for el in tp_from_bd:
            total_products.append([el.product_name, el.brand_url, el.product_price])
    except Exception as MultiValueDictKeyError:
        pass
    # Setting for search
    try:
        if request.POST['search_field'] != 'default':
            search_response = CatalogMobile.objects.filter(brand_name__icontains=request.POST['search_field']).order_by(options_to_display['order_by']).all()
            for el in search_response:
                total_products.append([el.product_name, el.brand_url, el.product_price])
    except Exception as MultiValueDictKeyError:
        pass

    statictic_library = []

    return render(request, 'scrapper/reports.html', {'total_products': total_products,
                                                     'brand_names_list': brand_names_list,
                                                     'display_brand_name': options_to_display['brand_name'],
                                                     'display_order_by': options_to_display['order_by']})


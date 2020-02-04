from scrapper.models import MobileProduct, CatalogMobile
from bs4 import BeautifulSoup
from django.utils import timezone
from pyvirtualdisplay import Display
from random import choice
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify
import os
import requests
import time


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
dir_path = os.path.dirname(os.path.realpath(__file__))
chromedriver = dir_path + '/drivers/chromedriver'
os.environ["webdriver.chrome.driver"] = chromedriver
display = Display(visible=0, size=(800, 600))
display.start()


class OnlinerBot:
    '''
    This class searches for all products by the entered name. For example, all phones company Apple.
    Technology: using the selenium library in the background, the Chrome browser launches
    and performs the necessary transformations with the data.
    '''
    def __init__(self):

        self.driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)
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
            '(лимитированная', 'серия)', '(песочный)', '(легендарная', 'модель)', 'коралл)',
            'Телефон', '(сиреневый)', 'dual', 'sim', 'Pebble', '(керамический', 'обсидиан)',
            '(пламенный', 'красный)', '(черная', 'керамика)', '(бургунди)', '(пурпурный)',
            '(серебристый', 'хром)', '(бордо)', '(белое', 'серебро)', '(розовый', ]

    def get_selenium_objects(self, brand_name):
        product_names_set = set()
        page = 1

        while True:
            url = "https://catalog.onliner.by/mobile?mfr%5B0%5D={}&page={}"

            self.driver.get(url.format(brand_name, str(page)))
            time.sleep(5)

            items = self.driver.find_elements_by_class_name("schema-product__part_2")
            time.sleep(2)

            if len(items) == 0:
                break

            for item in items:
                try:
                    div_block_title = item.find_element_by_class_name("schema-product__title")
                    name = div_block_title.find_element_by_tag_name('span').text.split()
                    product_name = ' '.join((i for i in name if i not in self.exception_words))
                except NameError:
                    product_name = ""

                try:
                    div_block_title = item.find_element_by_class_name("schema-product__title")
                    brand_url = div_block_title.find_element_by_tag_name('a').get_attribute('href')
                except NameError:
                    brand_url = ""

                try:
                    div_block_line = item.find_element_by_class_name("schema-product__line")
                    price = div_block_line.find_element_by_tag_name('span').text
                    product_price = int(price.split()[0].split(',')[0])
                except NoSuchElementException:
                    product_price = 0

                if product_name != '' and brand_url != '':
                    product_slug = slugify(brand_url)
                    scrapping_time = timezone.now()
                    new_product = [
                        product_name,
                        brand_url,
                        product_slug,
                        product_price,
                        scrapping_time
                    ]
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
            except Exception:
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

# ----------------------------------------------------------------


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
    try:
        p = get_proxy()
        proxy = {p['schema']: p['address']}
        r = requests.get(url, proxies=proxy, timeout=5)
    except:
        r = requests.get(url)
    return r.text


def get_product_mobile_data(html, brand_url):
    time.sleep(3)
    soup = BeautifulSoup(html, 'lxml')
    product_primary = soup.find('div', class_="product-primary-i")
    offer_description = product_primary.find('div', class_="offers-description")

    # description
    product_description = offer_description.find('div', class_="offers-description__specs")
    product_description = product_description.find('p').text.strip(' ')

    # prices
    prices_information = offer_description.find('div', id="product-prices-container")
    try:
        lowprice = int(prices_information.find_all('span')[0].text)
        highprice = int(prices_information.find_all('span')[1].text)
    except Exception:
        lowprice = 0
        highprice = 0

    # offers
    try:
        offercount = int(prices_information.find_all('span')[4].text)
    except Exception:
        offercount = 0

    result_data = [
        brand_url,
        product_description,
        lowprice,
        highprice,
        offercount
    ]
    return result_data


def record_session(result_data):
    settings = 'need to update'
    try:
        product_in_db = MobileProduct.objects.get(brand_url=result_data[0])
        if product_in_db:
            product_in_db.brand_url = result_data[0]
            product_in_db.product_description = result_data[1]
            product_in_db.lowprice = result_data[2]
            product_in_db.highprice = result_data[3]
            product_in_db.offercount = result_data[4]
            product_in_db.save()
        settings = 'updated'
    except Exception:
        pass

    if settings != 'updated':
        result = CatalogMobile.objects.get(brand_url=result_data[0])
        new_record = MobileProduct.objects.create(
            product_name=result,
            brand_url=result_data[0],
            product_description=result_data[1],
            lowprice=result_data[2],
            highprice=result_data[3],
            offercount=result_data[4],
        )
        new_record.save()


def find_all_brand_names():
    obj = CatalogMobile.objects.order_by('brand_name').all()
    brand_names_list = []
    for elem in obj:
        if elem.brand_name not in brand_names_list:
            brand_names_list.append(elem.brand_name)
    return brand_names_list


def request_handler(data):
    result_data = []
    data_list = data.split()
    for el in data_list:
        result_data.append(el.strip('.,/?()'))

    return result_data


from .models import MobileProduct, CatalogMobile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import csv
from scrapper.services.scrapper_bots import (
    OnlinerBot, find_all_brand_names, get_html, get_product_mobile_data,
    request_handler, record_session
)


def home_page(request):
    return render(request, 'scrapper/home.html')


def scrap_home(request):
    brand_names_list = find_all_brand_names()
    return render(request,
                  'scrapper/scrap_home.html',
                  {'brand_names_list': brand_names_list})


def scrap_result(request):
    page_settings = {'brand_name': 'default',
                     'product_page': 'default'}
    total_products = []
    product_pages = []
    result_data = []

    # if you input for example: apple (in first block)
    try:
        if request.POST['brand_name'] != '':
            page_settings['brand_name'] = request.POST['brand_name']
            brand_name = request.POST['brand_name']
            brand_name.strip('.,/?()').lower()
            new_session = OnlinerBot()
            new_session.get_selenium_objects(brand_name)
            new_session.update_db(brand_name)
            total_products = new_session.total_products
    except Exception:
        pass

    # if you input: https://catalog.onliner.by/mobile/apple/iphone4_16gb (in second block)
    try:
        if request.POST['product_page'] != '' and page_settings['brand_name'] == 'default':
            page_settings['product_page'] = request.POST['product_page']
            product_page = request.POST['product_page']
            urls = request_handler(product_page)
            for product_page in urls:
                result_bs = get_product_mobile_data(get_html(product_page), product_page)
                record_session(result_bs)
                result_data.append(result_bs)
    except Exception:
        pass

    # if you check some checkbox in result page
    try:
        if page_settings['product_page'] == 'default':
            for el in request.POST:
                if 'http' in request.POST[el]:
                    product_pages.append(request.POST[el])

            for product_page in product_pages:
                result_bs = get_product_mobile_data(get_html(product_page), product_page)
                record_session(result_bs)
                result_data.append(result_bs)
    except Exception:
        pass

    return render(request, 'scrapper/scrap_result.html', {
        'total_products': total_products,
        'product_pages': product_pages,
        'brand_name': page_settings['brand_name'],
        'product_page': page_settings['product_page'],
        'result_data': result_data
    })


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
        tp_from_bd = CatalogMobile.objects.filter(brand_name=options_to_display['brand_name']).all()
        tp_from_bd = tp_from_bd.order_by(options_to_display['order_by'])
        for el in tp_from_bd:
            total_products.append([el.product_name, el.brand_url, el.product_price])
    except Exception:
        pass
    # Setting for search
    try:
        if request.POST['search_field'] != 'default':
            response = CatalogMobile.objects.all()
            response = response.filter(brand_name__icontains=request.POST['search_field'])
            search_response = response.order_by(options_to_display['order_by'])
            for el in search_response:
                total_products.append([el.product_name, el.brand_url, el.product_price])
    except Exception:
        pass

    return render(request, 'scrapper/reports.html', {
        'total_products': total_products,
        'brand_names_list': brand_names_list,
        'display_brand_name': options_to_display['brand_name'],
        'display_order_by': options_to_display['order_by']
    })


def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dataset.csv"'
    q_set = CatalogMobile.objects.order_by('brand_name').all()

    writer = csv.writer(response)
    writer.writerow((
        'Brand name', 'Product name', 'URL', 'product_price', 'scrapping_time'
    ))
    for el in q_set:
        writer.writerow((
            el.brand_name,
            el.product_name,
            el.brand_url,
            el.product_price,
            el.scrapping_time
        ))
    return response


def clean_db(request):
    q_set_cm = CatalogMobile.objects.all()
    q_set_mp = MobileProduct.objects.all()
    for el in q_set_cm, q_set_mp:
        el.delete()

    return HttpResponseRedirect('/scrapper/')
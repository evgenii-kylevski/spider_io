from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from scrapper.views import home_page, scrap_home, scrap_result, reports_list
from scrapper.models import CatalogMobile, MobileProduct
import datetime
# from scrapper.urls import home, scrapper

# import ddt
# import mock

class TestUrls(SimpleTestCase):

    def test_home_page(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home_page)

    def test_scrap_home(self):
        url = reverse('scrapper')
        self.assertEquals(resolve(url).func, scrap_home)

    def test_scrap_result(self):
        url = reverse('scrap_result')
        self.assertEquals(resolve(url).func, scrap_result)

    def test_reports_list(self):
        url = reverse('reports')
        self.assertEquals(resolve(url).func, reports_list)


# @ddt.ddt
# class RecordTestClass(TestCase):
#
#     def setUp(self):
#         super(RecordTestClass, self).__init__()
#         self.client = Client()
#         self.user = models.User(first_name="maxim")
#         self.user.save()
#
#     def test_record_created(self):
#         """Test record creation returns 200"""
#         response = self.client.post('/create/',
#                                     {"title": 'maxim title',
#                                      "body": ' mybody',
#                                      "state": 'draft'})
#         self.assertEqual(response.status_code, 200)
#
#     def test_record_created_one(self):
#         response = self.client.post('/create/',
#                                     {"title": 'maxim title',
#                                      "body": ' mybody',
#                                      "state": 'draft'})
#         models.Record.objects.get()
#
#     @ddt.data("slug1", "slug2", "slug3")
#     def test_slug_created(self, title):
#         """Test slug={} created correctyly"""
#         response = self.client.post('/create/',
#                                     {"title": title,
#                                      "body": ' mybody',
#                                      "state": 'draft'})
#         self.assertEqual(models.Record.objects.get().slug,
#                          title)
#
#     @ddt.data(
#         ("slu g1", "slug1"),
#         ("s lu g 2", "slug2"),
#         ("sl ug3", "slug3"),
#     )
#     @ddt.unpack
#     def test_slug_created_correctly(self, title, expected_slug):
#         response = self.client.post('/create/',
#                                     {"title": title,
#                                      "body": ' mybody',
#                                      "state": 'draft'})
#         self.assertEqual(models.Record.objects.get().slug,
#                          expected_slug)
#
#     def _create_rec(self):
#         rec = models.Record(slug='slug',
#                             author=self.user,
#                             body='mybody')
#         rec.save()
#         return rec
#
#     def test_send_email(self):
#
#         rec = self._create_rec()
#
#         with mock.patch('feed.views.send_mail') as mail_mock:
#             response = self.client.post('/' + str(rec.id) + '/send/',
#                                         {"my_email": "ddd@dd.dd",
#                                          "address": "addr@dd.dd",
#                                          "comment": "adsfadsf"})
#         mail_mock.assert_called_once()
#
#     @mock.patch('feed.views.send_mail')
#     def test_send_email_decorated(self, mail_mock):
#         rec = self._create_rec()
#         response = self.client.post('/' + str(rec.id) + '/send/',
#                                     {"my_email": "ddd@dd.dd",
#                                      "address": "addr@dd.dd",
#                                      "comment": "adsfadsf"})
#         mail_mock.assert_called_once()
#         # mail_mock.assert_called_with()
#         # import pdb; pdb.set_trace()
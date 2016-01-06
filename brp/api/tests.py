from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
factory = APIRequestFactory()


class TestProtocolDatasourceAPI(APITestCase):

    fixtures = ['brp/api/fixtures/test_data.json']

    def test_has_content_length(self):
        '''returns should always have a content-length provided
        '''
        token = Token.objects.get(user__username='admin')
        url = reverse('pds-subject-list', args=[1])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(url, format='json')
        self.assertTrue(True, response.has_header('content-length'))


class TestProtocolAPI(APITestCase):

    fixtures = ['brp/api/fixtures/test_data.json']

    def test_protocol_with_no_datasources(self):
        token = Token.objects.get(user__username='admin')
        url = reverse('protocol-datasources-list', args=[2])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.data)

    def test_protocol_with_empty_datasource_configuration(self):
        token = Token.objects.get(user__username='admin')
        url = reverse('protocol-datasources-list', args=[1])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [{
                'data_source': {
                    'description': u"CHOP's REDCap Instance",
                    'url': u'https://redcap.chop.edu/api/',
                    'ehb_service_es_id': 1,
                    'desc_help': 'Please briefly describe this data source.',
                    'id': 1,
                    'name': u'REDCap'
                },
                'protocol': 'http://testserver/api/protocols/1/',
                'max_records_per_subject': -1,
                'driver': 0,
                'driver_configuration': '',
                'display_label': u'Health Data',
                'authorized': True,
                'path': u'Demo',
                'id': 1
            }],
            response.data
        )

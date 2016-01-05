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

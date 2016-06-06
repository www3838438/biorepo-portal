from django.test import TestCase
from django.contrib.auth.models import User
from .models.protocols import Organization, DataSource, Protocol, \
    ProtocolUser


class OrganizationTest(TestCase):

    def setUp(self):
        # This also calls out to the eHB to create an org.
        Organization.objects.create(name='TestOrg', subject_id_label='MRN')

    def test_immutable_key(self):
        '''
        Make sure Organization has an immutable key assigned
        '''
        org = Organization.objects.get(name='TestOrg', subject_id_label='MRN')
        self.assertEqual(org.immutable_key.key, 'C381K1T9G5SCOS5Z')

    def test_org_repr(self):
        org = Organization.objects.get(name='TestOrg', subject_id_label='MRN')
        self.assertEqual(str(org), 'TestOrg')

    def test_org_name(self):
        org = Organization.objects.get(name='TestOrg', subject_id_label='MRN')
        self.assertEqual(org.name, 'TestOrg')

    def test_org_subject_id_label(self):
        org = Organization.objects.get(name='TestOrg', subject_id_label='MRN')
        self.assertEqual(org.subject_id_label, 'MRN')

    def test_get_ehb_service_instance(self):
        '''
        Gets the record for this organization as maintained in the ehb service
        '''
        org = Organization.objects.get(name='TestOrg', subject_id_label='MRN')
        ehb_instance = org.getEhbServiceInstance()
        self.assertEqual(ehb_instance.name, 'TestOrg')

    def tearDown(self):
        org = Organization.objects.get(name='TestOrg', subject_id_label='MRN')
        org.delete()


class DataSourceTest(TestCase):

    def setUp(self):
        # This also calls out to the eHB to create a DataSource.
        DataSource.objects.create(
            name='TestDataSource',
            url='http://example.com',
            description='A test data source',
            ehb_service_es_id=1)

    def test_ds(self):
        pass

    def tearDown(self):
        ds = DataSource.objects.get(name='TestDataSource')
        ds.delete()


class ProtocolTest(TestCase):

    def setUp(self):
        # This also calls out to the eHB to create a DataSource.
        ds = DataSource.objects.create(
            name='TestDataSource',
            url='http://example.com',
            description='A test data source',
            ehb_service_es_id=1)
        # user = User.objects.create(
        #     username='TestUser',
        #     first_name='John',
        #     last_name='Doe',
        #     email='test_user@example.com'
        # )
        # p = ProtocolUser.objects.create(
        #     role=1,
        # )
        # p.datasources = [ds]
        # p.users = [user]
        # p.save()
        protocol = Protocol.objects.create(
            name='TestProtocol'
        )

    def test_protocol_group_name(self):
        p = Protocol.objects.get(name='TestProtocol')
        self.assertEqual(p.ehb_group_name(), 'BRP:C381K1T9G5SCOS5Z')

    def tearDown(self):
        p = Protocol.objects.get(name='TestProtocol')
        p.delete()


class ProtocolDataSourceTest(TestCase):

    def setUp(self):
        # This also calls out to the eHB to create a DataSource.
        pass

    def test_p(self):
        pass

    def tearDown(self):
        pass


class ProtocolDataSourceLinkTest(TestCase):

    def setUp(self):
        # This also calls out to the eHB to create a DataSource.
        pass

    def test_p(self):
        pass

    def tearDown(self):
        pass


class ProtocolUserTest(TestCase):

    def setUp(self):
        # This also calls out to the eHB to create a DataSource.
        pass

    def test_p(self):
        pass

    def tearDown(self):
        pass


class ProtocolUserCredentialsTest(TestCase):

    def setUp(self):
        # This also calls out to the eHB to create a DataSource.
        pass

    def test_p(self):
        pass

    def tearDown(self):
        pass

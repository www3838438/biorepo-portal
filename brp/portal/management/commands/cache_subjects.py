# encoding: utf-8
import datetime
import json

from portal.ehb_service_client import ServiceClient
from portal.models.protocols import Protocol, Organization, DataSource

from ehb_client.requests.exceptions import PageNotFound

from django.db import models
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.cache import get_cache

from portal.ehb_service_client import ServiceClient

from api.serializers import eHBSubjectSerializer

cache = get_cache('default')


class Command(BaseCommand):

    def getExternalRecords(self, pds, subject):
        # TODO: Need to cache this heavily!
        er_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD)
        er_label_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD_LABEL)
        lbls = er_label_rh.query()
        try:
            pds_records = er_rh.get(
                external_system_url=pds.data_source.url, path=pds.path, subject_id=subject['id'])
        except PageNotFound:
            pds_records = []

        r = []
        for ex_rec in pds_records:
            # Convert ehb-client object to JSON and then parse as py dict
            e = json.loads(ex_rec.json_from_identity(ex_rec))
            # Map label descriptions from the eHB to External Records
            for label in lbls:
                if e['label'] == label['id']:
                    if label['label'] == '':
                        e['label_desc'] = 'Record'
                    else:
                        e['label_desc'] = label['label']
            e['pds'] = pds.id
            r.append(e)

        return r

    def cache_records(self):
        protocols = Protocol.objects.all()
        for protocol in protocols:
            print 'Caching {}'.format(protocol)
            subjects = protocol.getSubjects()
            organizations = protocol.organizations.all()
            if subjects:
                subs = [eHBSubjectSerializer(sub).data for sub in subjects]
            else:
                return Response([])
            ehb_orgs = []
            # We can't rely on Ids being consistent across apps so we must
            # append the name here for display downstream.
            for o in organizations:
                ehb_orgs.append(o.getEhbServiceInstance())
            # Check if the protocol has external IDs configured. If so retrieve them
            manageExternalIDs = False

            protocoldatasources = protocol.getProtocolDataSources()

            for pds in protocoldatasources:
                if pds.driver == 3:
                    ExIdSource = pds
                    manageExternalIDs = True

            if manageExternalIDs:
                try:
                    config = json.loads(ExIdSource.driver_configuration)
                    if 'sort_on' in config.keys():
                        # er_label_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD_LABEL)
                        # lbl = er_label_rh.get(id=config['sort_on'])
                        lbl = ''
                        addl_id_column = lbl
                except:
                    pass

            for sub in subs:
                sub['external_records'] = []
                sub['external_ids'] = []
                for pds in protocoldatasources:
                    sub['external_records'].extend(self.getExternalRecords(pds, sub))
                if manageExternalIDs:
                    # Break out external ids into a separate object for ease of use
                    for record in sub['external_records']:
                        if record['external_system'] == 3:
                            sub['external_ids'].append(record)
                for ehb_org in ehb_orgs:
                    if sub['organization_id'] == ehb_org.id:
                        sub['organization_name'] = ehb_org.name
            cache_key = 'protocol{0}_sub_data'.format(protocol.id)
            cache.set(cache_key, json.dumps(subs))
            cache.expire(cache_key, 60*60*24)

    def handle(self, *args, **options):
        self.cache_records()

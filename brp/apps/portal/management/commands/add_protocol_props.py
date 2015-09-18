# encoding: utf-8
import datetime

from portal.ehb_service_client import ServiceClient
from portal.models.protocols import Protocol, Organization

from django.db import models
from django.conf import settings
from django.core.management.base import BaseCommand

from ehb_client.requests.group_request_handler import Group
from ehb_client.requests.exceptions import PageNotFound


class Command(BaseCommand):
    def _settings_prop(self, GROUP, KEY, default=None):
        PROTOCOL_PROPS = settings.PROTOCOL_PROPS
        if PROTOCOL_PROPS:
            GROUP_SETTINGS = PROTOCOL_PROPS.get(GROUP)
            if GROUP_SETTINGS:
                return GROUP_SETTINGS.get(KEY, default)
            else:
                return default
        else:
            return default

    def getProtocolGroup(self, protocol):
        gh = ServiceClient.get_rh_for(record_type=ServiceClient.GROUP)
        ck = self._settings_prop('CLIENT_KEY', 'key', '')
        n = 'BRP:'+protocol.immutable_key.key
        grp = gh.get(name=n)
        grp.client_key = ck
        # grp = Group(name = n, description = 'A BRP Protocol Group', is_locking=True, client_key=ck)
        # gh.create(grp)
        return (gh, grp)

    def delete_old_ehb_entities(self):
        '''
        This will remove the external_system entry for this protocol and the
        uneeded external records
        '''
        try:
            esrh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_SYSTEM)
            brp = esrh.get(url=ServiceClient.APP_URL)
            errh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD)

            print 'deleting records on external system: {0}'.format(brp.name)
            errh.delete(external_system_id=brp.id)

            print 'deleting external system: {0}'.format(brp.name)
            esrh.delete(id=brp.id)
        except PageNotFound:
            # This only happens if NO records are found when making the record
            # requests, indicates there are no subjects
            print '******** page not found in delete old ehb entities'

    def getProtocolSubjects(self, protocol):
        '''returns the Subject records for this protocol'''
        try:
            esrh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_SYSTEM)
            es = esrh.get(url=ServiceClient.APP_URL)
            return esrh.subjects(es.id, path=protocol.name)
        except PageNotFound:
            # This only happens if NO records are found when making the record
            # requests, indicates there are no subjects
            print '******** page not found for {0}, in get protocol subjects'.format(protocol.name)

        def migrate_subject(self, subject, protocol):
            try:
                # Create a Group for this subject / protocol combination
                orh = ServiceClient.get_rh_for(record_type=ServiceClient.ORGANIZATION)
                ehb_org = orh.get(id=subject.organization_id)
                brp_org = Organization.objects.get(name=ehb_org.name)
                gh = ServiceClient.get_rh_for(record_type=ServiceClient.GROUP)
                ck = self._settings_prop('CLIENT_KEY', 'key', '')
                n = 'BRP:'+protocol.immutable_key.key+':'+brp_org.immutable_key.key+':'+subject.organization_subject_id
                grp = Group(name=n,
                            description='A BRP Protocol Subject Record Group',
                            is_locking=True,
                            client_key=ck)
                gh.create(grp)
                print 'created subject records group: {0} for subject: {1} on protocol: {2}'.format(
                    n,
                    subject.organization_subject_id,
                    protocol.name)
                # Add the subjects records to this group
                errh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD)
                records = errh.get(subject_id=subject.id, path=protocol.name)
                print 'subject {0}, {1}, id={2} has the following records:'.format(
                    subject.last_name,
                    subject.first_name,
                    subject.id)
                for rec in records:
                    print 'id={0}, path={1}, ex_sys_id={2}, subject_id={3}'.format(
                        rec.id,
                        rec.path,
                        rec.external_system_id,
                        rec.subject_id
                    )
                    gh.add_records(grp, records)
                print 'added {0} records for subject: {1} on protocol: {2} to group: {3}'.format(
                    len(records),
                    subject.organization_subject_id,
                    protocol.name,
                    grp.name
                )
        except Exception:
            print '********failed to move subject records for ', subject.organization_subject_id

    def migrate_orgs(self):
        for org in Organization.objects.all():
            org.save()  # This should generate the immutable keys

    def migrate(self):
        self.migrate_orgs()
        for protocol in Protocol.objects.all():
            print '----------------------------------'
            print 'protocol ', protocol.name
            protocol.save()  # This should cause the protocol to create key and create it's group
            print 'created immutable key: {0} for protocol {1}'.format(
                protocol.immutable_key.key,
                protocol.name)

            gh, group = self.getProtocolGroup(protocol)
            print 'created protocol subject group {0} with id={1}'.format(
                group.name,
                group.id)
            subjects = self.getProtocolSubjects(protocol)
            if subjects:
                print 'adding {0} subjects to protocol {1} using group {2}'.format(
                    str(len(subjects)),
                    protocol.name,
                    group.name
                )
                gh.add_subjects(group, subjects)
                for subject in subjects:
                    self.migrate_subject(subject, protocol)
            else:
                print '********no subjects for protocol ', protocol.name
            print '----------------------------------'
        self.delete_old_ehb_entities()

        def handle(self, *args, **options):
            self.migrate()

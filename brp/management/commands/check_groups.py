import csv
from datetime import date, datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models.protocols import Protocol, Organization
from api.ehb_service_client import ServiceClient
from api.utilities import SubjectUtils

from ehb_client.requests.exceptions import RequestedRangeNotSatisfiable
from http.client import BadStatusLine
User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'protocol',
            nargs='?',
            default=None,
            type=int,
            help='Specify a protocol to check.')
        parser.add_argument(
            '--continue',
            action='store_true',
            default=False,
            help='Continue to next protocols from the Protocol specified above'
        )
        parser.add_argument(
            '--csv',
            action='store_true',
            default=False,
            help='Generate a csv file containing warnings.'
        )

    def handle(self, *args, **options):

        if options['protocol']:
            if options['continue']:
                protocols = Protocol.objects.filter(id__gte=options['protocol']).order_by('id').all()
            else:
                try:
                    protocols = Protocol.objects.filter(id=options['protocol']).all()
                except Protocol.DoesNotExist:
                    print('Protocol specified does not exist')
                    return
        else:
            protocols = Protocol.objects.order_by('id').all()
        g_rh = ServiceClient.get_rh_for(record_type=ServiceClient.GROUP)
        errors = []
        msg = None
        for protocol in protocols:
            print('Checking {0} (ID:{1}) Group: {2}'.format(
                protocol.name,
                protocol.id,
                protocol.ehb_group_name()))
            try:
                g_rh.get(name=protocol.ehb_group_name())
            except RequestedRangeNotSatisfiable:
                msg = ('Unable to find expected group: {0}'.format(protocol.ehb_group_name()))
                errors.append(msg)
                print(msg)
                msg = None
            # Check for pds groups
            subjects = protocol.getSubjects()
            if subjects:
                for subject in subjects:
                    try:
                        SubjectUtils.get_protocol_subject_record_group(protocol, subject)
                    except RequestedRangeNotSatisfiable as e:
                        msg = ('Warning: Group not found under Protocol: {0} Group name expected: {1}'.format(
                            protocol.name,
                            e.errmsg
                        ))
                    except Organization.DoesNotExist:
                        msg = ('Warning: Could not find associated Organization for protocol: {0}, eHB Org ID: {1} Likely eHB/BRP organizaiton mismatch'.format(
                            protocol.name,
                            subject.organization_id
                        ))

                    except BadStatusLine:
                        msg = ('Warning: Malformed Group Detected for Protocol: {0} Subject ID: {1} Likely Bad Organization ID'.format(
                            protocol.name,
                            subject.id
                        ))
                    if msg:
                        errors.append(msg)
                        print(msg)
                        msg = None

        if csv:
            with open('group_report_{0}.csv'.format(datetime.now().strftime('%Y%m%d.%H:%M.%S')), 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=' ',
                                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for error in errors:
                    csv_writer.writerow([error])

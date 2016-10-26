import { createStore, applyMiddleware, compose } from 'redux';
import thunkMiddleware from 'redux-thunk';
import rootReducer from '../reducers';
import createLogger  from 'redux-logger';

const middlewares = [thunkMiddleware];

if (process.env.NODE_ENV === 'development') {
  const logger = createLogger();
  middlewares.push(logger);
}

const testState = {
  protocol: {
    isFetching: false,
    items: [{
      id: 1,
      name: 'Demonstration Protocol',
      users: ['http://localhost:8000/api/users/1/'],
      data_sources: ['http://localhost:8000/api/datasources/1/', 'http://localhost:8000/api/datasources/2/', 'http://localhost:8000/api/datasources/3/'],
      protocol_data_sources:   'http://localhost:8000/api/protocols/1/data_sources/',
      subjects:   'http://localhost:8000/api/protocols/1/subjects/',
      organizations:   'http://localhost:8000/api/protocols/1/organizations/'
    }, {
      id:   2,
      name:   'Demonstration Protocol II',
      users:   ['http://localhost:8000/api/users/1/'],
      data_sources:   ['http://localhost:8000/api/datasources/1/', 'http://localhost:8000/api/datasources/2/', 'http://localhost:8000/api/datasources/3/'],
      protocol_data_sources:   'http://localhost:8000/api/protocols/2/data_sources/',
      subjects:   'http://localhost:8000/api/protocols/2/subjects/',
      organizations:   'http://localhost:8000/api/protocols/2/organizations/'
    }],
    activeProtocolId:   1,
    orgs:   [{
      id:   1,
      name:   'Amazing Children\'s Hospital',
      subject_id_label:   'Record ID'
    }]
  },
  subject:   {
    isFetching: false,
    items:   [{
      id:   1,
      first_name:   'John',
      last_name:   'Sample',
      organization_subject_id:   '42424242',
      dob:   '2000-01-01',
      modified:   '2015-09-29T12:09:05.202000',
      created:   '2015-09-29T12:09:05.202000',
      external_records:   [{
        label:   1,
        subject:   1,
        path:   'Demo',
        id:   1,
        external_system:   1,
        record_id:   'S891XSB0XD1NKRPF:I5CPQ07I5',
        label_desc:   'Record',
        pds:   1,
        created:   '2015-09-29 13:51:16.189000',
        modified:   '2015-09-29 13:51:16.190000'
      }, {
        label:   1,
        subject:   1,
        path:   'Demo',
        id:   2,
        external_system:   1,
        record_id:   'S891XSB0XD1NKRPF:XM5VUKTNY',
        label_desc:   'Record',
        pds:   1,
        created:   '2015-09-29 13:51:16.189000',
        modified:   '2016-10-17 10:56:45.740581'
      }, {
        label:   1,
        subject:   1,
        path:   'Demo',
        id:   3,
        external_system:   1,
        record_id:   'S891XSB0XD1NKRPF:N330M7OL5',
        label_desc:   'Record',
        pds:   1,
        created:   '2016-10-07 15:03:03.080619',
        modified:   '2016-10-07 15:03:03.080637'
      }, {
        label:   1,
        subject:   1,
        path:   'demo_exrecs',
        id:   4,
        external_system:   3,
        record_id:   '2222',
        label_desc:   'Record',
        pds:   3,
        created:   '2016-10-17 10:53:04.619335',
        modified:   '2016-10-17 10:53:04.619383'
      }],
      external_ids:   [{
        label:   1,
        subject:   1,
        path:   'demo_exrecs',
        id:   4,
        external_system:   3,
        record_id:   '2222',
        label_desc:   'Record',
        pds:   3,
        created:   '2016-10-17 10:53:04.619335',
        modified:   '2016-10-17 10:53:04.619383'
      }],
      organization:   1,
      organization_name:   'Amazing Children\'s Hospital',
      organization_subject_id_validation:   '42424242'
    }, {
      id:   2,
      first_name:   'T',
      last_name:   'T',
      organization_subject_id:   '334',
      dob:   '2014-08-05',
      modified:   '2016-10-17T10:57:45.600855',
      created:   '2016-10-17T10:57:45.600836',
      external_records:   [{
        label:   1,
        subject:   2,
        path:   'Demo',
        id:   5,
        external_system:   1,
        record_id:   'WFXECEASIEEDLRJI:HUCNPN3QP',
        label_desc:   'Record',
        pds:   1,
        created:   '2016-10-17 10:57:56.598643',
        modified:   '2016-10-17 10:57:56.598681'
      }],
      external_ids:   [],
      organization:   1,
      organization_name:   'Amazing Children\'s Hospital',
      organization_subject_id_validation:   '334'
    }],
    activeSubject:   null,
    activeSubjectRecords:   [],
    newSubject:   {
      organization:   null,
      dob:   null,
      first_name:   null,
      last_name:   null,
      organization_subject_id:   null,
      organization_subject_id_validation:   null
    },
    isSaving:   false,
    showInfoPanel:   false,
    showActionPanel:   false,
    addRecordMode:   false,
    linkMode:   false,
    newFormErrors:   {
      server:   [],
      form:   []
    },
    updateFormErrors:   {
      server:   [],
      form:   []
    },
    addSubjectMode:   false
  },
  pds:   {
    isFetching:   false,
    activePDS:   null,
    availableLinkTypes:   {},
    items:   [{
      id:   3,
      protocol:   'http://localhost:8000/api/protocols/1/',
      data_source:   {
        id:   3,
        name:   'External Identifiers',
        url:   'http://example.com/noop/',
        desc_help:   'Please briefly describe this data source.',
        description:   'Placeholder for external IDs',
        ehb_service_es_id:   3
      },
      path:   'demo_exrecs',
      driver:   3,
      driver_configuration:   {
        sort_on:   2,
        labels:   [
          [2, 'SSN']
        ]
      },
      display_label:   'External IDs',
      max_records_per_subject:   1,
      subjects:   'http://localhost:8000/api/protocoldatasources/3/subjects/',
      authorized:   true
    }, {
      id:   1,
      protocol:   'http://localhost:8000/api/protocols/1/',
      data_source:   {
        id:   1,
        name:   'REDCap',
        url:   'https://redcap.chop.edu/api/',
        desc_help:   'Please briefly describe this data source.',
        description:   'CHOP\'s REDCap Instance',
        ehb_service_es_id:   1
      },
      path:   'Demo',
      driver:   0,
      driver_configuration:   {
        form_data:   {
          meal_description_form:   [0, 1, 1, 1],
          baseline_visit_data:   [1, 0, 0, 0]
        },
        unique_event_names:   ['visit_arm_1', 'breakfast_at_visit_arm_1', 'lunch_at_visit_arm_1', 'dinner_at_visit_arm_1'],
        links:   [1],
        record_id_field_name:   'study_id',
        event_labels:   ['Visit Baseline', 'Breakfast', 'Lunch', 'Dinner'],
        labels:   [
          [1, 'Record']
        ]
      },
      display_label:   'Health Data',
      max_records_per_subject:   -1,
      subjects:   'http://localhost:8000/api/protocoldatasources/1/subjects/',
      authorized:   true
    }, {
      id:   2,
      protocol:   'http://localhost:8000/api/protocols/1/',
      data_source:   {
        id:   2,
        name:   'LIMS',
        url:   'https://example.com/api/',
        desc_help:   'Please briefly describe this data source.',
        description:   'Laboratory Management',
        ehb_service_es_id:   2
      },
      path:   'demo_lab',
      driver:   1,
      driver_configuration:   {
        labels:   [
          [1, 'Record']
        ]
      },
      display_label:   'Sample Check In',
      max_records_per_subject:   -1,
      subjects:   'http://localhost:8000/api/protocoldatasources/2/subjects/',
      authorized:   false
    }]
  },
  record:   {
    isFetching:   false,
    isCreating:   false,
    items:   [],
    activeRecord:   null,
    activeLinks:   [],
    pendingLinkedRecord:   null,
    editLabelMode:   false,
    selectedLabel:   null,
    selectedLinkType:   null,
    selectLinkTypeModal:   false,
    linkError:   null,
    newRecordError:   null
  },
  notification:   {
    items:   []
  }
}
const store = compose(applyMiddleware(...middlewares))(createStore)(rootReducer, testState);

export default store;

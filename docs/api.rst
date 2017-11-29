API
================================================

The Biorepository Portal provides a RESTful API for retrieving and updating data in the application.

Organizations
-------------

Coming Soon

Datasources
-----------

Protocols
---------

.. http:get:: /api/protocols/(int: protocol_id)/

The protocol by `protocol_id`

**Example Request**:

.. sourcecode:: http

    GET /api/protocols/1/ HTTP/1.1
    Host: example.com
    Accept: application/json

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    {
        "id": 1,
        "name": "Demonstration Protocol",
        "users": [
            "http://example.com/api/users/1/"
        ],
        "data_sources": [
            "http://example.com/api/datasources/1/",
            "http://example.com/api/datasources/2/",
            "http://example.com/api/datasources/3/"
        ],
        "protocol_data_sources": "http://example.com/api/protocols/1/data_sources/",
        "subjects": "http://example.com/api/protocols/1/subjects/",
        "organizations": "http://example.com/api/protocols/1/organizations/"
    }

.. http:get:: api/protocols/(int: protocol_id)/subjects/

The subjects associated with protocol `protocol_id` including their external records.

Typically this endpoint should be cached as it is expensive due to the retrieval of external records from the eHB.

**Example Request**:

.. sourcecode:: http

      GET /api/protocols/1/subjects/ HTTP/1.1
      Host: example.com
      Accept: application/json

**Example Response**:

.. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "organization_id": 1,
            "organization_subject_id": "909999",
            "dob": "2000-01-01",
            "modified": "2016-05-13T14:05:37.930839",
            "created": "2016-05-13T14:05:37.930797",
            "external_records": [
                {
                    "label_desc": "SSN",
                    "created": "2016-05-13 14:13:10.837416",
                    "pds": 3,
                    "modified": "2016-05-13 14:13:10.837454",
                    "label": 2,
                    "record_id": "1111115",
                    "path": "demo_exrecs",
                    "external_system": 3,
                    "id": 1,
                    "subject": 1
                },
                {
                    "label_desc": "Record",
                    "created": "2016-05-13 14:13:10.837416",
                    "pds": 1,
                    "modified": "2016-05-13 14:13:10.837454",
                    "label": 1,
                    "record_id": "1111115",
                    "path": "test_study:redcap",
                    "external_system": 1,
                    "id": 2,
                    "subject": 1
                }
            ],
            "external_ids": [
                {
                    "label_desc": "SSN",
                    "created": "2016-05-13 14:13:10.837416",
                    "pds": 3,
                    "modified": "2016-05-13 14:13:10.837454",
                    "label": 2,
                    "record_id": "1111115",
                    "path": "demo_exrecs",
                    "external_system": 3,
                    "id": 1,
                    "subject": 1
                }
            ],
            "organization_name": "Amazing Children's Hospital"
        }
      ]

.. http:get:: /api/protocols/<id>/data_sources/


**Example Request**:

.. sourcecode:: http

      GET /api/protocols/1/data_sources/ HTTP/1.1
      Host: example.com
      Accept: application/json

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
        {
            "id": 3,
            "protocol": "http://example.com/api/protocols/1/",
            "data_source": {
                "id": 3,
                "name": "External Identifiers",
                "url": "http://example.com/noop/",
                "desc_help": "Please briefly describe this data source.",
                "description": "Placeholder for external IDs",
                "ehb_service_es_id": 3
            },
            "path": "demo_exrecs",
            "driver": 3,
            "driver_configuration": {
                "labels": [
                    [
                        2,
                        "SSN"
                    ]
                ],
                "sort_on": 2
            },
            "display_label": "External IDs",
            "max_records_per_subject": 2,
            "subjects": "http://example.com/api/protocoldatasources/3/subjects/",
            "authorized": true
        },
        {
            "id": 1,
            "protocol": "http://example.com/api/protocols/1/",
            "data_source": {
                "id": 1,
                "name": "REDCap",
                "url": "https://redcap.chop.edu/api/",
                "desc_help": "Please briefly describe this data source.",
                "description": "CHOP's REDCap Instance",
                "ehb_service_es_id": 1
            },
            "path": "Demo",
            "driver": 0,
            "driver_configuration": {
                "links": [
                    1,
                    2
                ],
                "labels": [
                    [
                        1,
                        "Record"
                    ]
                ],
                "event_labels": [
                    "Visit Baseline",
                    "Breakfast",
                    "Lunch",
                    "Dinner"
                ],
                "record_id_field_name": "study_id",
                "form_data": {
                    "meal_description_form": [
                        0,
                        1,
                        1,
                        1
                    ],
                    "baseline_visit_data": [
                        1,
                        0,
                        0,
                        0
                    ]
                },
                "unique_event_names": [
                    "visit_arm_1",
                    "breakfast_at_visit_arm_1",
                    "lunch_at_visit_arm_1",
                    "dinner_at_visit_arm_1"
                ]
            },
            "display_label": "Health Data",
            "max_records_per_subject": -1,
            "subjects": "http://example.com/api/protocoldatasources/1/subjects/",
            "authorized": true
        },
        {
            "id": 2,
            "protocol": "http://example.com/api/protocols/1/",
            "data_source": {
                "id": 2,
                "name": "LIMS",
                "url": "https://example.com/api/",
                "desc_help": "Please briefly describe this data source.",
                "description": "Laboratory Management",
                "ehb_service_es_id": 2
            },
            "path": "demo_lab",
            "driver": 1,
            "driver_configuration": {
                "labels": [
                    [
                        1,
                        "Record"
                    ]
                ]
            },
            "display_label": "Sample Check In",
            "max_records_per_subject": -1,
            "subjects": "http://example.com/api/protocoldatasources/2/subjects/",
            "authorized": false
        }
    ]

.. http:get:: /api/protocols/<id>/organizations/

**Example Request**:

.. sourcecode:: http

      GET /api/protocols/1/organizations/ HTTP/1.1
      Host: example.com
      Accept: application/json

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
        {
            "id": 1,
            "name": "Amazing Children's Hospital",
            "subject_id_label": "Record ID"
        }
    ]

.. http:get:: /api/protocols/(int: protocol_id)/subjects/(int: subject_id)/

Retrieve details about a single subject on a specific protocol.

**Example Request:**

**Example Response:**



.. http:post:: /api/protocols/(int: protcol_id)/subjects/create/`

Create a subject and add them to the specified protocol.

**Example Request:**

.. sourcecode:: http

    POST /api/protocols/1/subjects/create HTTP/1.1
    Host: example.com
    Content-Type: application/json

    {
        "first_name": "John",
        "last_name": "Doe",
        "organization_subject_id": "123123123",
        "organization": "1",
        "dob": "2000-01-01"
    }

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    {

    }

Protocol Datasources
--------------------

Coming Soon


Contents:

.. toctree::
   :maxdepth: 2

Data Sources
============

Data Sources are external systems that the Biorepository Portal
utilizes for downstream data capture.

A Data Source represents an external data source used within the Biorepository
Portal. It is the link between the BRP app and the ehb-service. The field
ehb_service_es_id is the id of the ExternalSystem record stored in the
ehb-service corresponding to this DataSource. The name field should match
the name field in the ExternalSystem record.

Attributes:

* **Data Source Name**: The name of the Data Source (unique)
* **URL**: The URL of the Data Source (unique) must match the corresponding ExternalSystem URL in the eHB.
* **Description**: A brief description of the Data Source.
* **External System ID**: A non-editable field storing the ID of the corresponding External System in the eHB. This is retrieved when the Data Source is created. If the External System does not exist in the eHB it is created.

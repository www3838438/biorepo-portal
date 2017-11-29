Protocol Data Source Credentials
================================

The Protocol Data Source Credential object holds information necessary for a Portal user to access a given DataSource for a given protocol.

* **Protocol**: The Protocol associated with these credentials.
* **Protocol Data Source**: The Protocol Datasource associated with these credentials.
* **User**: The base User associated.
* **Protocol User**: The Protocol User associated.
* **Data Source Username**: The user name to be passed downstream to the datasource. (Used with Nautilus driver).
* **Data Source Password**: The password or API key to be passed downstream to the datasource. In the case of REDCap, only this field is used and populated with the user's REDCap API key -- user name is left blank.

.. note::

    A user's REDCap API token is not valid until they have logged in to REDCap at least once.

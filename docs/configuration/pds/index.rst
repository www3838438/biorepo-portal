Protocol Data Source
====================

Protocol Data Sources tie together a Data Source to a Protocol.

An example of a configured Protocol Data Source might allow for data entry on a
set of REDCap forms in a REDCap Project or the association of Sample Kits in a
Nautilus LIMs system.

* **Protocol**: The Protocol this Protocol Data Source is associated with.
* **Data Source**: The Data Source this Protocol Data Source is associated with.
* **Path**: This *should* be unique for each Project using the same data source. It can be thought of as a record namespace.
* **Driver**: The driver being used to facilitate data entry. This driver should correspond with the Data Source. Currently supported drivers are:

    * REDCap Client
    * Nautilus Driver
    * Phenotype Intake Driver
    * External Record ID Management Driver

* **Driver Configuration**: A JSON string that passes configuration information down to each driver. The configuration depends on the driver selected and must be valid JSON. Please refer to the REDCap and Nautilus examples below.
* **Display Label**: How the Protocol Data Source should be labeled in the Biorepository Portal for end users.
* **Max Records Per Subject**: The maximum amount of records that should be allowed for a Subject on a Protocol Data Source. Use `-1` to specify an unlimited amount of records allowed.

Contents:

.. toctree::
   :maxdepth: 3

   REDCap Example <redcap>
   Nautilus Example <nautilus>

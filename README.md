## Quickstart

The Biorepository Portal contains a [docker-compose](https://www.docker.com/docker-compose) file which defines a `brp` service to quickly spin up a demonstration instance of the portal. This demo consists of the Portal itself, redis, as well as a companion instance of [electronic Honest Broker](https://github.com/chop-dbhi/ehb-service).

Run:

`docker-compose up brp`

Demonstration accounts for both the Portal and the eHB have a user name of `admin@email.chop.edu` and a password of `Chopchop1234` (case sensitive).

## Introduction

#### What is the Biorepository Portal?

The Biorepository Portal (BRP) is the main client for the Electronic Honest Broker.
It provides an interface that displays protocols with associated patients and systems
(also called datasources) that each patient has a record in. It can also, depending
on the datasource driver, provide an interface within the application to that
datasource, or link out to the system externally. An example of an application
embedded within the driver would be the REDCap form interface provided within the
BRP. An example of a driver that just links out to an external system is the
phenotype intake driver.

## What is the ehb-service?

This biorepository-portal presents a unified interface that shows protocol names,
the patients on each protocol, and the external systems that each patient on
each protocol has records in. To accomplish this, it accesses the ehb-service
where all Protected Health Information (PHI) and identifiers used in external
systems are actually stored. See the wiki for implementation details and for a
better understanding of services provided by the BRP versus services provided
by the ehb-service.


## Workflow

A user logs into the BRP and sees a list of Projects (Protocols) they have
access to, which is determined by Protocol User objects.

They click on a Protocol and see a list of Patients in that protocol.
Next to each patient, there is a button for each external system
(also called Datasource) on that Protocol. These buttons are configured by
creating a Protocol Datasource object. Whether or not a button is enabled
(clickable) depends on whether the logged in user has credentials in the system
for the associated Datasource, which is configured by creating a Protocol User
Credentials object. This associates a User and a Protocol Datasource (see the
next section for details). Clicking on a given button brings up a page with a
list of records that the patient has on that external system (or shows an empty
list if the patient has no records yet), and a button to create a new record.

Clicking on a given record in that list opens up a page controlled by the
datasource driver. This could show an entire embedded application (in the case
of the REDCap driver) or just link out to an external system.

### Adding subjects to a protocol
Patients can be added to a Protocol on the Protocol Screen by clicking the
"Add Subject" button. This makes a request to the ehb-service adding the
user to the Protocol and creating the user in the system if they do not exist
yet.  

Whether or not the user already exists in the ehb-service system is determined
by the MRN (organization wide patient identifier). This patient information,
while added using the biorepository-portal is not stored in the biorepository-portal's
database, it just tells the ehb-service to add the user to the Protocol.
Later on, to display the Protocol page that lists users on a Protocol, the
biorepository-portal will ask the ehb-service for all patients on the Protocol,
and list them on the page, but it does not store that information. This is a
slight simplification of the process, see the
[wiki](http://github.com/chop-dbhi/biorepo-portal/wiki/Biorepository-portal-and-ehb-service:-Separation-of-Concerns)
for more details.

## Organization/Protocol/Datasource Hierarchy

<center>
<img src="http://github.com/chop-dbhi/biorepo-portal/raw/master/doc/datamodel.png"/>
</center>

Organizations have one or more Protocols. Multiple organizations may be on the
same protocol. To link Datasources with a Protocol, you create a Protocol
Datasource.  For example, there may be protocol called Study A linked to
organizations CHOP and Boston's Children's with 1 REDCap Datasource (tied to
the Protocol by creating a Protocol Datasource linking the REDCap Datasource
with Study A).

Finally, user credential objects are tied to the Protocol Datasource object. For
each user that might login, you need to configure credentials for each external
system on each protocol they need to access. For example, if you have a Protocol
with a REDCap Datasource, you will need to set the user's REDCap API key in a
Protocol User Credentials object. This ties together the User, the Protocol, the
Datasource, and the API key credential. If that is not done than the button to
the REDCap Datasource will be disabled.

## Drivers
Datasources are defined in the biorepository-portal, but the drivers that access
those datasources are defined in the ehb-datasources repository.

To add a new type of driver, you need to add it to the list in
`brp/apps/portal/models/protocols.py`.

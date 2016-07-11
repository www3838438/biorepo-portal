Organizations
=============

Organizations usually represent a Hospital but semantically they
can refer to any group of subjects. You may have a Protocol
that contains two "Organizations" each of represents a grouping
of subjects within a Hospital i.e. Coded and Non-Coded subjects.

When creating a new Organization the Biorepository Portal will
attempt to create a matching Organization in the connected
electronic Honest Broker (eHB). The eHB has no concept of
Protocols but utilizes Organizations to create what it refers to
as Subject Groups, and Subject Record Groups.

An Organization has two attributes:

* **Name**: The name of the organization (must be unique)
* **Subject ID Label**: The label to be applied to a Subject's ID i.e. MRN

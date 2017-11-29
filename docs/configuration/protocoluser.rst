Protocol User
=============

The Protocol User object ties a User to a specific Protocol.

Logins to the Biorepository Portal are throttled. After 10 attempts a user's
account becomes deactivated. There is a management command to ease the reactivation
of a user is has been locked out:

`./manage.py reactivate_user <user_id>`

This will change the user to "active" status and remove their attempts from the
session cache.

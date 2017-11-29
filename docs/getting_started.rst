Getting Started
================================================

The Biorepository Portal consists of two main parts:

* A Django application that provides models, the django admin interface to create and update those models, and a RESTful API to expose those models
* A ReactJS based front-end application which consumes the API exposed by the Django application.

To get our application up and running we will have to create a Python environment for the Django application to run in and install the necessary javascript dependencies to build our front-end application.

Requirements
------------

* Python 2.7+
* Node + NPM

.. note:: If you are a Docker user you can build the javascript application within a container skipping the need to setup Node and NPM on your system.

.. code-block:: bash

    # To install dependencies and create production bundle
    docker run -it --rm -v $(pwd):/opt/app -w /opt/app node:4.4.7 npm install && npm run build
    # To install dependencies, watch files for changes and automatically rebuild
    docker run -it --rm -v $(pwd):/opt/app -w /opt/app node:4.4.7 npm install && npm run watch

This command will mount your current directory into a container, install the necessary dependencies for the front-end application, build the application and output it to the path specified in the production webpack configuration.

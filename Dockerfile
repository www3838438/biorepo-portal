FROM python:2.7.8-wheezy

MAINTAINER Tyler Rivera "riverat2@email.chop.edu"

RUN apt-get update -qq --fix-missing
RUN apt-get install -y\
    build-essential\
    git-core\
    libldap2-dev\
    libpq-dev\
    libsasl2-dev\
    libssl-dev\
    libxml2-dev\
    libxslt1-dev\
    libffi-dev\
    openssl\
    python-dev\
    python-setuptools\
    wget\
    zlib1g-dev\
    postgresql-client

RUN pip install "Django>=1.6,<1.7"
RUN pip install "south==1.0.1"
RUN pip install "django-environ==0.3.0"
RUN pip install "django-session-security==2.2.1"
RUN pip install "django-markdown-deux==1.0.5"
RUN pip install "djangorestframework==3.1.1"
RUN pip install "djangorestframework-jwt==1.5.0"
RUN pip install "git+https://github.com/chop-dbhi/ehb-client.git"
RUN pip install "git+https://github.com/chop-dbhi/ehb-datasources.git"
RUN pip install "psycopg2==2.5.4"
RUN pip install "python-memcached==1.53"
RUN pip install "python-ldap==2.4.19"
RUN pip install "django-siteauth==0.9b1"
RUN pip install "git+https://github.com/bruth/django-registration2.git#egg=django-registration2"
RUN pip install "markdown2==2.3.0"
RUN pip install "raven==5.0.0"
RUN pip install "django-redis==4.2.0"
RUN pip install uWSGI

ENV APP_ENV test

ADD . /opt/app
ADD test.env_example /opt/app/test.env

# Ensure all python requirements are met
RUN pip install -r /opt/app/requirements.txt

CMD ["/opt/app/scripts/run.sh"]

EXPOSE 8000

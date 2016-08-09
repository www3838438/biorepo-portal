FROM alpine:3.3

RUN apk add --update \
    bash \
    python \
    python-dev \
    py-pip \
    build-base \
    git \
    openldap-dev \
    linux-headers \
    pcre-dev \
    musl-dev \
    postgresql-dev \
    mailcap \
  && rm -rf /var/cache/apk/*

RUN pip install "Django>=1.9.6,<1.10"
RUN pip install "django-environ>=0.4.0,<0.5"
RUN pip install "django-markdown-deux>=1.0.5,<1.1"
RUN pip install "django-session-security>=2.3.2,<2.4"
RUN pip install "django_redis>=4.4.3,<4.5"
RUN pip install "djangorestframework>=3.3.3,<3.4"
RUN pip install "djangorestframework-jwt>=1.5.0,<1.6"
RUN pip install "git+https://github.com/chop-dbhi/ehb-client.git@bd60fa0925e57d41cea0343e6d71d9340cfe4e3e#egg=ehb_client-master"
RUN pip install "git+https://github.com/chop-dbhi/ehb-datasources.git@5de3cb0#egg=ehb_datasources-master"
RUN pip install "python-ldap>=2.4.25,<2.5"
RUN pip install "gunicorn>=19,<20"
RUN pip install "psycopg2>=2.6.1,<2.7"
RUN pip install "python-logstash>=0.4.6,<0.5"
RUN pip install "dj-static>=0.0.6,<0.1.0"


ENV APP_ENV test
ADD . /opt/app/
ADD test.env_example /opt/app/test.env

CMD ["/opt/app/bin/run.sh"]

EXPOSE 8000

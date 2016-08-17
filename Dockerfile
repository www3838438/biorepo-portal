FROM alpine:3.3

RUN apk add --update \
    bash \
    python3 \
    python3-dev \
    py-pip \
    build-base \
    git \
    openldap-dev \
    linux-headers \
    pcre-dev \
    musl-dev \
    postgresql-dev \
    mailcap \
  && rm -rf /var/cache/apk/* && \
  python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache

RUN pip3 install "Django>=1.9.6,<1.10"
RUN pip3 install "django-environ>=0.4.0,<0.5"
RUN pip3 install "django-markdown-deux>=1.0.5,<1.1"
RUN pip3 install "django-session-security>=2.3.2,<2.4"
RUN pip3 install "django_redis>=4.4.3,<4.5"
RUN pip3 install "djangorestframework>=3.3.3,<3.4"
RUN pip3 install "djangorestframework-jwt>=1.5.0,<1.6"
RUN pip3 install "git+https://github.com/chop-dbhi/ehb-client.git@bd60fa0925e57d41cea0343e6d71d9340cfe4e3e#egg=ehb_client-master"
RUN pip3 install "git+https://github.com/chop-dbhi/ehb-datasources.git@5de3cb0#egg=ehb_datasources-master"
RUN pip3 install "ldap3>=1.4.0,<1.5"
RUN pip3 install "gunicorn>=19,<20"
RUN pip3 install "psycopg2>=2.6.1,<2.7"
RUN pip3 install "python-logstash>=0.4.6,<0.5"
RUN pip3 install "dj-static>=0.0.6,<0.1.0"


ENV APP_ENV test
ADD . /opt/app/
ADD test.env_example /opt/app/test.env

CMD ["/opt/app/bin/run.sh"]

EXPOSE 8000

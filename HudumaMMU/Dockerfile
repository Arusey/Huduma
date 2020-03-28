FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV=$($LAZY_SUDO cat /proc/$PID/environ | tr '\0' '\n' | grep = | grep -v my_variable_with_spaces)


RUN mkdir /HudumaMMU

WORKDIR /HudumaMMU

ADD . /HudumaMMU

RUN pip install -r requirements.txt


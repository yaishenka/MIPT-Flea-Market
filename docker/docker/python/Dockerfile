FROM python:3.7

MAINTAINER yaishenka

RUN apt-get install git
RUN git clone https://github.com/yaishenka/MIPT-Flea-Market /srv/MIPT_Flea_Market

WORKDIR /srv/MIPT_Flea_Market

RUN git checkout dev

COPY ./MIPT_Flea_Market /srv/MIPT_Flea_Market

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN ln -s /usr/local/lib/python3.7/site-packages/django/contrib/admin/static/admin /srv/MIPT_Flea_Market/static
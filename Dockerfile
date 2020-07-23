FROM python:3.8.3

EXPOSE 8000
ENV PYTHONUNBUFFERED=0
RUN useradd -ms /bin/bash user
RUN chgrp -R 0 /home/user && chmod -R g=u /home/user
ENV APP_HOME /home/user
WORKDIR $APP_HOME
ADD requirements.txt requirements.txt
RUN pip install -U -r requirements.txt
COPY . .
USER user
#RUN python manage.py collectstatic --no-input
# ENTRYPOINT python manage.py migrate && uwsgi --ini uwsgi.ini
#ENTRYPOINT python manage.py makemigrations && python manage.py migrate && uwsgi --ini uwsgi.ini
ENTRYPOINT uwsgi --ini uwsgi.ini

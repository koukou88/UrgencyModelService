# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7.2-alpine

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

ADD . /ml-service

#RUN apt-get update && apt-get update && apt-get install -y gcc build-essential autoconf cmake libtool git python-dev

#RUN python -m pip install --upgrade pip setuptools wheel
#RUN mkdir /mybin && echo '/mybin directory created'
#ENV PATH="/mybin:${PATH}"
#RUN cd /mybin && ln -sf $(which gcc) x86_64-linux-gnu-gcc && x86_64-linux-gnu-gcc -v

RUN pip install -r ml-service/requirements-docker.txt


#RUN python -m spacy download en_core_web_md
#RUN python -m nltk.downloader stopwords

EXPOSE 80

CMD ["python", "ml-service/manage.py", "runserver", "0.0.0.0:80"]
FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY  ./wait-for-it.sh /usr/wait-for-it.sh
RUN ["chmod", "+x", "/usr/wait-for-it.sh"]
COPY ./pollynesia_project/ /code/
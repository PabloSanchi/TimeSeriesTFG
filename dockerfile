FROM python

RUN mkdir -p /home/app

WORKDIR /home/app

COPY requirements.txt /home/app

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
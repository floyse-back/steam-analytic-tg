FROM python:3.12

WORKDIR /src

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

COPY prestart.sh ./prestart.sh

RUN chmod +x ./prestart.sh

ENTRYPOINT ["/src/prestart.sh"]

CMD ["python","-m","src.main"]
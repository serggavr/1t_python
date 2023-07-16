FROM python:3
WORKDIR .
ADD parser.py /
RUN pip install pip install requests
RUN pip install pip pip install beautifulsoup4
COPY . .
CMD [ "python", "./parser.py" ]
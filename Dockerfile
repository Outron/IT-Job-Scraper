FROM python:3.12

WORKDIR /IT-Job-Scraper

COPY requirements.txt .

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["bash"]






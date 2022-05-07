FROM python:3

WORKDIR /opt/swatch
COPY requirements.txt /opt/swatch/requirements.txt

ENV OPENCV_VERSION="4.5.1"

RUN pip install -r requirements.txt

WORKDIR /opt/swatch/
ADD swatch .

EXPOSE 4500

CMD ["python3", "-u", "-m", "app"]

FROM python:3

# build swatch backend
WORKDIR /opt/swatch
COPY requirements.txt /opt/swatch/requirements.txt
COPY requirements_dev.txt /opt/swatch/requirements_dev.txt

ENV OPENCV_VERSION="4.5.1"

RUN pip install -r requirements.txt

WORKDIR /opt/swatch/
ADD swatch swatch/

EXPOSE 4500

# build swatch frontend
FROM nginx
COPY docker/rootfs /

ADD web/build/libs/project-1.0.0-SNAPSHOT web/

EXPOSE 4550

# general docker

CMD ["python3", "-u", "-m", "swatch"]
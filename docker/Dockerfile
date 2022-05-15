FROM nginx

FROM python:3

# install dependencies
COPY requirements.txt /requirements.txt
COPY requirements_dev.txt /requirements_dev.txt

ENV OPENCV_VERSION="4.5.1"

RUN pip install -r requirements.txt

# build swatch frontend
WORKDIR /opt/swatch/

COPY swatch swatch/
COPY web/dist frontend/

COPY docker/rootfs /

# general docker

EXPOSE 4500

CMD ["python3", "-u", "-m", "swatch"]
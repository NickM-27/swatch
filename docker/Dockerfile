FROM nginx

FROM python:3

# install dependencies
COPY requirements.txt /requirements.txt
COPY requirements_dev.txt /requirements_dev.txt

ENV OPENCV_VERSION="4.5.1"

RUN pip install -r requirements.txt

COPY --from=nginx /usr/local/nginx/ /usr/local/nginx/

# build swatch frontend
WORKDIR /opt/swatch/

ADD swatch swatch/
ADD web/build/libs/project-1.0.0-SNAPSHOT web/

COPY docker/rootfs /

# general docker

EXPOSE 4500
EXPOSE 4550

CMD ["python3", "-u", "-m", "swatch"]
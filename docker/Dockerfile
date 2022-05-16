FROM crzynik/swatch-nginx:latest as nginx

FROM python:3

# install dependencies
COPY requirements.txt /requirements.txt
COPY requirements_dev.txt /requirements_dev.txt

ENV OPENCV_VERSION="4.5.1"

RUN pip install -r requirements.txt

COPY --from=nginx /usr/local/nginx/ /usr/local/nginx/

# build swatch frontend
WORKDIR /opt/swatch/

COPY swatch swatch/
COPY web/build/web frontend/

COPY docker/rootfs /

# general docker

EXPOSE 4500

COPY startup.sh /
RUN chmod +x /startup.sh

CMD ["/startup.sh"]
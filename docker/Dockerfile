FROM python:3

WORKDIR /opt/swatch
COPY requirements.txt /opt/swatch/requirements.txt

ENV OPENCV_VERSION="4.5.1"

RUN if [ "${TARGETARCH}" = "arm" ]; \
    then echo "[global]" > /etc/pip.conf \
    && echo "extra-index-url=https://www.piwheels.org/simple" >> /etc/pip.conf; \
    fi

RUN pip install -r requirements.txt

WORKDIR /opt/swatch/
ADD swatch swatch/

EXPOSE 4500

CMD ["python3", "-u", "-m", "swatch"]

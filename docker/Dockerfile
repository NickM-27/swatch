FROM python:3

WORKDIR /opt/swatch

ENV OPENCV_VERSION="4.5.1"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir  matplotlib  pillow numpy opencv-python-headless && \
    pip install --no-cache-dir Flask requests pydantic PyYAML waitress colorthief

WORKDIR /opt/swatch/
ADD swatch .

EXPOSE 4500

CMD ["python3", "-u", "-m", "app"]

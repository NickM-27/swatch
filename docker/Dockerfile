FROM python:3

WORKDIR /opt/swatch

ENV OPENCV_VERSION="4.5.1"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir  matplotlib  pillow numpy opencv-python-headless Flask requests pydantic PyYAML

WORKDIR /opt/swatch/
ADD swatch .

EXPOSE 5000

CMD ["python3", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
#!/bin/bash

/usr/local/nginx/sbin/nginx &
python3 -u -m swatch

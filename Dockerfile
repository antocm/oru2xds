FROM python:3.10-alpine AS build

LABEL maintainer="digiplan.pt@gmail.com"

RUN apk add --no-cache bash shadow

WORKDIR /usr/local/lib/python3.10/site-packages/oru2xds

RUN python -m pip install --upgrade pip
RUN pip install oru2xds

CMD [ "python3", "oru2xds.py" ]

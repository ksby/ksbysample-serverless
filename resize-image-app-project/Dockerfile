FROM lambci/lambda:build-python3.8

COPY resize_service/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN pip install moto

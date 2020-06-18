FROM lambci/lambda:build-python3.8

COPY shared_package_layer/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN pip install moto

ENV PYTHONPATH "${PYTHONPATH}:/opt/python"

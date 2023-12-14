FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /mypan
WORKDIR /mypan

RUN pip install pip -U -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

ADD . /mypan/

RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

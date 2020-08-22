FROM python:3.8.2
ENV TZ=Asia/Shanghai
MAINTAINER banyan.cheung@gmail.com
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com --no-cache-dir -r requirements.txt
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY . .
CMD [ "python", "./run.py" ]

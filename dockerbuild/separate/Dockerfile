FROM python:3
ENV TZ="Asia/Shanghai"
RUN date

WORKDIR /usr/src/app
RUN mkdir ./scaledata


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

CMD [ "python", "-u", "./script/MT-client-separate.py" ]
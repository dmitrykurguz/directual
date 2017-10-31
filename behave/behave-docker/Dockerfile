FROM python:3

WORKDIR /usr/src/app/behave

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

VOLUME ["/usr/src/app/behave"]

# RUN cd behave
# COPY . .

CMD [ "behave" ]

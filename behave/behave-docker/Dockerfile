FROM python:3

WORKDIR /usr/src/app/behave

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

VOLUME ["/usr/src/app/behave"]
VOLUME ["/usr/src/app/reports"]

# RUN cd behave
# COPY . .

CMD [ "behave" ]

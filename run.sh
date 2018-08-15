#!/bin/bash



docker pull selenoid/vnc:chrome_62.0
docker-compose up mongo redis redis_object_cache postgres zookeeper kafka
docker-compose up web_ui selenoid nginx_proxy

rm -rf ./reports
docker-compose up behave
allure serve ./reports

# 
## also cat start
# processor
# distributor
# delay_processor
# operations

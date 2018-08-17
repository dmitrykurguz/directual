#!/bin/bash



docker pull selenoid/vnc:chrome_62.0
docker-compose up -d mongo redis redis_object_cache postgres zookeeper kafka
docker-compose up -d selenoid
docker-compose up metadata-service mongodb-service
docker-compose up web_ui

rm -rf ./reports
docker-compose up nginx_proxy behave
allure serve ./reports

behave -Dapp_address=http://localhost:8080
➜  cases git:(plt-870-test-remote) ✗ behave -Dapp_address=http://localhost:8080 -f allure_behave.formatter:AllureFormatter -o reports

# 
## also cat start
# processor
# distributor
# delay_processor
# operations

#!/bin/bash



docker pull selenoid/vnc:chrome_62.0
docker-compose up -d mongo redis redis_object_cache postgres zookeeper kafka
docker-compose up -d selenoid
docker-compose up metadata-service mongodb-service
docker-compose up web_ui

rm -rf ./reports
docker-compose up nginx_proxy behave
allure serve ./reports

➜  cases git:(plt-870-test-remote) ✗ 

behave -w -Dapp_address=http://localhost:8081 -Dmetadata_address=localhost:12345 -Dmongodb_address=localhost:12341

➜  cases git:(plt-870-test-remote) ✗ behave -Dapp_address=http://localhost:8080 -f allure_behave.formatter:AllureFormatter -o reports



behave -Dapp_address=http://localhost:8081 -Dmetadata_address=localhost:12345 -Dmongodb_address=localhost:12341 -f allure_behave.formatter:AllureFormatter -o reports

# 
## also cat start
# processor
# distributor
# delay_processor
# operations

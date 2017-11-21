#!/bin/bash

#COMPOSE_PROJECT_NAME=qacore docker-compose -f docker-compose-infra.yml -f docker-compose-web-ui.yml -f docker-compose-behave.yml -f docker-compose-selenoid.yml up --abort-on-container-exit --exit-code-from behave
#COMPOSE_PROJECT_NAME=qacore docker-compose -f docker-compose-infra.yml -f docker-compose-web-ui.yml -f docker-compose-behave.yml -f docker-compose-selenoid.yml down


#docker network inspect qacore_default   and run stop/rm containers of browser, delete network



export WEB_UI_IMAGE_TAG=local-test-web-ui:5
export COMPOSE_PROJECT_NAME=qacorelocal

echo "using project name $COMPOSE_PROJECT_NAME"
echo "using web-ui tag: ${WEB_UI_IMAGE_TAG}"

export TEST_APP_ID=test_app_id
export TEST_APP_SECRET=test_app_secret_12!@
export WEB_UI_IMAGE=${WEB_UI_IMAGE_TAG}
export DATASOURCE=PostgreSQLDS
export DATASOURCE_PARAMS=


#docker-compose -f docker-compose-infra.yml -f docker-compose-web-ui.yml -f docker-compose-behave.yml -f docker-compose-selenoid.yml up --abort-on-container-exit --force-recreate
#docker-compose -f docker-compose-infra.yml -f docker-compose-web-ui.yml -f docker-compose-behave.yml -f docker-compose-selenoid.yml down


docker-compose  -f docker-compose-behave-local.yml -f docker-compose-selenoid.yml up --abort-on-container-exit --force-recreate


allure serve ./reports

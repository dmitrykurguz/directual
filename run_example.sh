#!/bin/bash

#COMPOSE_PROJECT_NAME=qacore docker-compose -f docker-compose-infra.yml -f docker-compose-web-ui.yml -f docker-compose-behave.yml -f docker-compose-selenoid.yml up --abort-on-container-exit --exit-code-from behave
#COMPOSE_PROJECT_NAME=qacore docker-compose -f docker-compose-infra.yml -f docker-compose-web-ui.yml -f docker-compose-behave.yml -f docker-compose-selenoid.yml down


#docker network inspect qacore_default   and run stop/rm containers of browser, delete network





#export WEB_UI_IMAGE_TAG=gitlab.directual.com:5005/platform/directual-server/web-ui:2.0.19


export WEB_UI_IMAGE_TAG=test/local-test-web-ui:5
export COMPOSE_PROJECT_NAME=qacorelocal

echo "using project name $COMPOSE_PROJECT_NAME"
echo "using web-ui tag: ${WEB_UI_IMAGE_TAG}"

export TEST_APP_ID=test_app_id
export TEST_APP_SECRET=test_app_secret_12!@
export WEB_UI_IMAGE=${WEB_UI_IMAGE_TAG}
export DATASOURCE=PostgreSQLDS
export DATASOURCE_PARAMS=
export STAGE_HOST=hp-dev01.directual.tech


#docker-compose -f docker-compose-infra.yml -f docker-compose-web-ui.yml -f docker-compose-behave.yml -f docker-compose-selenoid.yml up --abort-on-container-exit --force-recreate

docker-compose -f docker-compose-infra-pg.yml -f docker-compose-web-ui-stage.yml -f docker-compose-behave.yml -f docker-compose-selenoid.yml up --abort-on-container-exit --force-recreate
# sleep 10
# docker-compose  -f up --abort-on-container-exit --force-recreate


#docker-compose -f docker-compose-infra.yml -f docker-compose-web-ui.yml -f docker-compose-behave.yml -f docker-compose-selenoid.yml down
docker-compose -f docker-compose-infra-pg.yml -f docker-compose-web-ui-stage.yml -f docker-compose-behave.yml -f docker-compose-selenoid.yml down

allure serve ./reports






#1 - docker-compose -f docker-compose-infra.yml -f docker-compose-web-ui.yml up --abort-on-container-exit --force-recreate
#2 - 



# docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v ${HOME}:/root -e OVERRIDE_HOME=${HOME} aerokube/cm:latest-release selenoid start --vnc --tmpfs 128 -g "--container-network qacorelocal_default"
# docker run --rm -v /Users/onexdrk/directual/qa-core/behave/cases:/usr/src/app/behave --name behave-cases --network=qacorelocal_default behave behave -D hub=http://selenoid:4444/wd/hub -Dapp_address=http://web_ui:8080
#!/bin/bash

COMPOSE_PROJECT_NAME=qacore docker-compose -f docker-compose-infra.yml -f docker-compose-web-ui.yml -f docker-compose-behave.yml -f docker-compose-selenoid.yml up --abort-on-container-exit --exit-code-from behave
COMPOSE_PROJECT_NAME=qacore docker-compose -f docker-compose-infra.yml -f docker-compose-web-ui.yml -f docker-compose-behave.yml -f docker-compose-selenoid.yml down


#docker network inspect qacore_default   and run stop/rm containers of browser, delete network
#allure serve ./reports

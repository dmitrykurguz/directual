#!/bin/bash

rm -rf reports
behave -Dapp_address=http://localhost:8081 -f allure_behave.formatter:AllureFormatter -o reports

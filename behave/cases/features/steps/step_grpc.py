import time
import sys
import os
import pickle
import requests
import json
import grpc

from google.protobuf import empty_pb2


# sys.path.append('./directualproto')

from directualproto . CommonRequestResponse_pb2 import NetworkIDWithStructSysNameRequest

from flatten_json import flatten_json
from behave import given, when, then
from step_utils import readCookieFromCache, appAddress, paramFromConfig, debug, logError, safe, deepgetattr, assertEq, debugProto


@given('вызываем "metadata-service.FindBySysName" и проверяем')
def step_impl(context):
    def impl():
        step_params = json.loads(context.text)

        request = NetworkIDWithStructSysNameRequest()
        request.networkID = step_params['request']['networkID']
        request.sysName = step_params['request']['sysName']

        debugProto('request', request)
        result = context.metadataServiceStub.FindBySysName(request)
        debugProto('response', result)

        assertion = flatten_json(step_params['assert'], '.')

        for assertKey, assertValue in assertion.items():
            # extract value from StringValue
            objValue = deepgetattr(result, assertKey)
            assertEq(objValue, assertValue)
    
    safe(impl)
    


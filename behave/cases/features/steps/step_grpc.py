import time
import sys
import os
import pickle
import requests
import json
import grpc

from google.protobuf import empty_pb2
from google.protobuf.wrappers_pb2 import StringValue



from directualproto . CommonRequestResponse_pb2 import NetworkIDWithStructSysNameRequest, NetworkIDWithStructSysNameRequestAndUserIDRequest, CreateStructureRequest
from directualproto . DTO_pb2 import StructureDTO

from flatten_json import flatten_json
from behave import given, when, then
from step_utils import readCookieFromCache, appAddress, paramFromConfig, debug, logError, safe, deepgetattr, assertEq, debugProto


@given('в networkID "{networkID:d}" удаляем структуру "{sysName}"')
@when('в networkID "{networkID:d}" удаляем структуру "{sysName}"')
def step_impl(context, networkID, sysName):
    def impl():
        request = NetworkIDWithStructSysNameRequestAndUserIDRequest()
        request.networkID = networkID
        request.sysName = sysName
        request.userID = 0

        debugProto('request', request)
        result = context.metadataServiceStub.RemoveBySysName(request)
        debugProto('response', result)

    safe(impl)


@given('в networkID "{networkID:d}" создаем структуру "{sysName}"')
@when('в networkID "{networkID:d}" создаем структуру "{sysName}"')
def step_impl(context, networkID, sysName):
    def impl():
        dto = StructureDTO(
            sysName = StringValue(value = sysName),
            name = StringValue(value = '%s structure' % sysName)
        )

        request = CreateStructureRequest(
            networkID = networkID,
            struct = dto,
            userID = 0
        )

        debugProto('request', request)
        result = context.metadataServiceStub.Create(request)
        debugProto('response', result)

    safe(impl)

@given('ищем структуру и проверяем')
@then('ищем структуру и проверяем')
def step_impl(context):
    def impl():
        step_params = json.loads(context.text)

        request = NetworkIDWithStructSysNameRequest()
        request.networkID = step_params['request']['networkID']
        request.sysName = step_params['request']['sysName']

        debugProto('request', request)
        result = context.metadataServiceStub.FindBySysName(request)
        debugProto('response', result)

        # TODO extract below
        assertion = flatten_json(step_params['assert'], '.')

        for assertKey, assertValue in assertion.items():
            # extract value from StringValue
            objValue = deepgetattr(result, assertKey)
            assertEq(objValue, assertValue)
    
    safe(impl)


import time
import sys
import os
import pickle
import requests
import json
import grpc

from google.protobuf import empty_pb2
from google.protobuf.wrappers_pb2 import StringValue, Int64Value, Int32Value, BoolValue, DoubleValue


from directualproto . CommonRequestResponse_pb2 import NetworkIDWithStructSysNameRequest, NetworkIDWithStructSysNameRequestAndUserIDRequest, CreateStructureRequest, ScenarioObjectDTOWrapperWithStructInfo
from directualproto . DTO_pb2 import StructureDTO, ScenarioObjectDTOWrapper, StructureInfoDTO, FieldsValues, FieldDataValue

from flatten_json import flatten_json
from behave import given, when, then
from step_utils import readCookieFromCache, appAddress, paramFromConfig, debug, logError, safe, deepgetattr, assertEq, debugProto, addToCache, readFromCache


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


@given('в networkID "{networkID:d}" создаем структуру "{sysName}" с полями')
@when('в networkID "{networkID:d}" создаем структуру "{sysName}" с полями')
def step_impl(context, networkID, sysName):
    def impl():
        fieldInfo = context.text
        

        # for fieldName, dataType in step_params.items():


        dto = StructureDTO(
            sysName = StringValue(value = sysName),
            name = StringValue(value = '%s structure' % sysName),
            jsonObjectRaw = StringValue(value = fieldInfo),
            indexEnabled = BoolValue(value = False)
        )

        request = CreateStructureRequest(
            networkID = networkID,
            struct = dto,
            userID = 0
        )

        debugProto('request', request)
        result = context.metadataServiceStub.Create(request)
        debugProto('response', result)

        addToCache(structCacheKey(networkID, sysName, 'id'), result.id.value)

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


@then('в networkID "{networkID:d}" создаем объект в структуре "{structName}"')
def step_impl(context, networkID, structName):
    def impl():
        structID = readFromCache(structCacheKey(networkID, structName, 'id'))
        debug('previously created struct id is %s' % structID)

        step_params = json.loads(context.text)
        id = step_params['request']['id']
        data = step_params['request']['data']
        fieldValues = dataToFieldsValues(data)

        request = ScenarioObjectDTOWrapperWithStructInfo(
            dto = ScenarioObjectDTOWrapper(
                networkID=Int64Value(value = networkID),
                structID=Int64Value(value = structID),
                objectID=StringValue(value = id),
                data=fieldValues
            ),
            structInfo = dogStructInfo()
        )
        debugProto('request', request)
        result = context.mongodbServiceStub.Save(request)
        debugProto('response', result)

        assertion = flatten_json(step_params['assert'], '.')
        for assertKey, assertValue in assertion.items():
            # extract value from StringValue
            objValue = deepgetattr(result, assertKey)
            assertEq(objValue, assertValue)

    
    safe(impl)




def dogStructInfo():
    obj = StructureInfoDTO(
        idFieldSysName=StringValue(value = 'id'),
        dataTypeByName={}
    )
    return  obj


def structCacheKey(networkID, sysName, field):
    result = '%s_%s_%s' % (networkID, sysName, field)
    return result


def dataToFieldsValues(data):
    result = dict(
        map(lambda kv: (kv[0], valueToFieldDataValue(kv[1])), data.items()))
    response = FieldsValues(values = result)
    return response


def valueToFieldDataValue(value):
    if type(value) is str:
        return FieldDataValue(
            stringValue=StringValue(
                value=str(value)
            )
        )
    if type(value) is bool:
        return FieldDataValue(
            booleanValue=BoolValue(
                value=bool(value)
            )
        )
    if type(value) is int:
        return FieldDataValue(
            intValue=Int32Value(
                value=int(value)
            )
        )
    if type(value) is float:
        return FieldDataValue(
            doubleValue=DoubleValue(
                value=float(value)
            )
        )

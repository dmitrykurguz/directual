import time
import sys
import os
import pickle
import requests
import json
# import python_generated_sources
import grpc

# from python_generated_sources import DTO_pb2
# from python_generated_sources import CommonRequestResponse_pb2
# from python_generated_sources 

from google.protobuf import empty_pb2

from MetadataRemoteService_pb2_grpc import MetadataRemoteServiceStub
from CommonRequestResponse_pb2 import NetworkIDWithStructSysNameRequest

from flatten_json import flatten_json
from behave import given, when, then
from step_utils import readCookieFromCache, appAddress, paramFromConfig, debug, logError, safe, deepgetattr, assertEq, debugProto


@given('вызываем "metadata-service.FindBySysName" и проверяем')
def step_impl(context):
    def impl():
        step_params = json.loads(context.text)

        with grpc.insecure_channel('localhost:12345') as channel:
            stub = MetadataRemoteServiceStub(channel)
            empty = empty_pb2.Empty()
            #result = stub.Ping(empty)
            request = NetworkIDWithStructSysNameRequest()
            request.networkID = step_params['request']['networkID']
            request.sysName = step_params['request']['sysName']

            debugProto('request', request)
            result = stub.FindBySysName(request)  # DTO_pb2.StructureOptionDTO
            debugProto('response', result)
            
            assertion = flatten_json(step_params['assert'], '.')

            for assertKey, assertValue in assertion.items():
                # extract value from StringValue
                objValue = deepgetattr(result, assertKey)
                assertEq(objValue, assertValue)
    
    safe(impl)
    


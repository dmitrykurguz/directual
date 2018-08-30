import time
import sys
import os
import pickle
import requests
import json
import grpc
import uuid

from google.protobuf import empty_pb2
from google.protobuf.wrappers_pb2 import StringValue, Int64Value, Int32Value, BoolValue, DoubleValue


from directualproto . CommonRequestResponse_pb2 import NetworkIDWithStructSysNameRequest, NetworkIDWithStructSysNameRequestAndUserIDRequest, CreateStructureRequest, ScenarioObjectDTOWrapperWithStructInfo, ExistsRequest, FieldsWithDataRequest, FindObjectRequest, NetworkIDWithScenarioObjectListRequestWithStructInfo, NetworkIDWithScenarioObjectListRequest, SimpleAggregateRequest, GenerateReportStructureRequest, BuildReportRequest, NetworkIDWithStructIDRequest, ProcessObjectRequest
from directualproto . DTO_pb2 import StructureDTO, ScenarioObjectDTOWrapper, StructureInfoDTO, FieldsValues, FieldDataValue, BasicScenarioObjDTO, ExpressionResultDto, ExpressionResultType, SET, FilterDTO, PaginatorDTO, ScenarioObjectListDTO, ReportSettingsDTO, DataType, ID, STRING, NUMBER, DECIMAL, BOOLEAN, DATE, ARRAY, LINK, ARRAY_LINK

from flatten_json import flatten_json
from behave import given, when, then
from step_utils import readCookieFromCache, appAddress, paramFromConfig, debug, logError, safe, deepgetattr, assertEq, debugProto, addToCache, readFromCache


@given('в networkID "{networkID:d}" удаляем структуру "{sysName}"')
@when('в networkID "{networkID:d}" удаляем структуру "{sysName}"')
@then('в networkID "{networkID:d}" удаляем структуру "{sysName}"')
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


def typeToDataType(typeStr):
    if typeStr == 'id':
        return ID
    if typeStr == 'string':
        return STRING
    if typeStr == 'number':
        return NUMBER
    if typeStr == 'decimal':
        return DECIMAL
    if typeStr == 'boolean':
        return BOOLEAN
    if typeStr == 'date':
        return DATE
    if typeStr == 'array':
        return ARRAY
    if typeStr == 'link':
        return LINK
    if typeStr == 'arrayLink':
        return ARRAY_LINK


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
            indexEnabled = BoolValue(value = True)
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


        step_params = json.loads(context.text)
        dataTypeByName = dict(map(lambda x: (x['sysName'], typeToDataType(x['dataType'])), step_params))

        print('dataTypeByName')
        print(dataTypeByName)
        print(dataTypeByName['id'])
        print(type(dataTypeByName['id']))

        obj = StructureInfoDTO(
            idFieldSysName=StringValue(value = 'id'),
            dataTypeByName=dataTypeByName
        )

        cacheStructInfo(networkID, sysName, obj)

    safe(impl)


def cacheStructInfo(networkID, sysName, obj):
    addToCache(structCacheKey(networkID, sysName,
                              '_sturctInfo'), obj.SerializeToString())

def readStructInfo(networkID, sysName):
    data = readFromCache(structCacheKey(networkID, sysName, '_sturctInfo'))
    result = StructureInfoDTO()
    result.ParseFromString(data)
    return result



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
        structInfo = readStructInfo(networkID, structName)
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
            structInfo=structInfo
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


def fieldValuesToDtoWithStructInfo(networkID, structID, id, fieldValues):
    dto = fieldValueToScenarioObjectDTOWrapper(networkID, structID, id, fieldValues)
    return ScenarioObjectDTOWrapperWithStructInfo(dto=dto)


def fieldValueToScenarioObjectDTOWrapper(networkID, structID, id, fieldValues):
    return ScenarioObjectDTOWrapper(
        networkID=Int64Value(value=networkID),
        structID=Int64Value(value=structID),
        objectID=StringValue(value=id),
        data=fieldValues)



@given('в networkID "{networkID:d}" создаем множество объектов в структуре "{structName}"')
@when('в networkID "{networkID:d}" создаем множество объектов в структуре "{structName}"')
@then('в networkID "{networkID:d}" создаем множество объектов в структуре "{structName}"')
def step_impl(context, networkID, structName):
    def impl():
        structID = readFromCache(structCacheKey(networkID, structName, 'id'))

        step_params = json.loads(context.text)
        dataItems = step_params['request']

        structInfoByStruct = {}
        structInfo = readStructInfo(networkID, structName)
        structInfoByStruct[structID] = structInfo


        items = map(lambda x: (x['id'], dataToFieldsValues(x['data'])), dataItems)
        
        debug(items)

        dtoList = list(map(lambda kv: fieldValueToScenarioObjectDTOWrapper(
            networkID, structID, kv[0], kv[1]), items))

        request = NetworkIDWithScenarioObjectListRequestWithStructInfo(
            dto=NetworkIDWithScenarioObjectListRequest(
                networkID=networkID,
                scenarioObjects=ScenarioObjectListDTO(values=dtoList)
            ),
            structInfoByStruct=structInfoByStruct,
            
        )
        debugProto('request', request)
        result = context.mongodbServiceStub.SaveBatch(request)
        debugProto('response', result)
        
    safe(impl)


@then('в networkID "{networkID:d}" генерируем "{count:d}" объектов в структуре "{structName}"')
def step_impl(context, networkID, count, structName):
    def impl():
        structID = readFromCache(structCacheKey(networkID, structName, 'id'))

        step_params = json.loads(context.text)
        pattern = step_params['pattern']

        structInfo = readStructInfo(networkID, structName)
        structInfoByStruct = {}
        structInfoByStruct[structID] = structInfo

        items = map(lambda idx: (templatePattern(pattern['id'], idx), dataToFieldsValues(
            templatePattern(pattern['data'], idx))), range(count))

        dtoList = list(map(lambda kv: fieldValueToScenarioObjectDTOWrapper(
            networkID, structID, kv[0], kv[1]), items))

        request = NetworkIDWithScenarioObjectListRequestWithStructInfo(
            dto=NetworkIDWithScenarioObjectListRequest(
                networkID=networkID,
                scenarioObjects=ScenarioObjectListDTO(values=dtoList)
            ),
            structInfoByStruct=structInfoByStruct,

        )
        debugProto('request', request)
        result = context.mongodbServiceStub.SaveBatch(request)
        debugProto('response', result)

    safe(impl)

@when('в networkID "{networkID:d}" существует объект в структуре "{structName}" с id="{id}"')
@then('в networkID "{networkID:d}" существует объект в структуре "{structName}" с id="{id}"')
def step_impl(context, networkID, structName, id):
    def impl():
        structID = readFromCache(structCacheKey(networkID, structName, 'id'))
        request = ExistsRequest(
            networkID=networkID,
            structID=structID,
            ids=[id]
        )
        
        debugProto('request', request)
        result = context.mongodbServiceStub.Exists(request)
        debugProto('response', result)
        assertEq(result.value, True)

        request2 = BasicScenarioObjDTO(
            networkID=networkID,
            structID=structID,
            objectID=id
        )

        debugProto('request 2', request2)
        result2 = context.mongodbServiceStub.Exist(request2)
        debugProto('response 2', result2)

        assertEq(result2.value, True)


    safe(impl)


@when('в networkID "{networkID:d}" изменим поля в структуре "{structName}" с id="{id}"')
def step_impl(context, networkID, structName, id):
    def impl():
        step_params = json.loads(context.text)
        data = step_params['request']['data']
        structID = readFromCache(structCacheKey(networkID, structName, 'id'))
        structInfo = readStructInfo(networkID, structName)
        changeFields=dataToChangeFieldObjects(data)
        request = FieldsWithDataRequest(
            networkID=networkID,
            structID=structID,
            objectID=id,
            who="behave",
            structInfo=structInfo,
            fields=changeFields
        )

        debugProto('request', request)
        result = context.mongodbServiceStub.ChangeFieldObject(request)
        debugProto('response', result)

        assertion = flatten_json(step_params['assert'], '.')
        for assertKey, assertValue in assertion.items():
            # extract value from StringValue
            objValue = deepgetattr(result, assertKey)
            assertEq(objValue, assertValue)


    safe(impl)


@then('в networkID "{networkID:d}" ищем по структуре "{structName}"')
@when('в networkID "{networkID:d}" ищем по структуре "{structName}"')
def step_impl(context, networkID, structName):
    def impl():
        step_params = json.loads(context.text)
        structID = readFromCache(structCacheKey(networkID, structName, 'id'))

        assertForFilters(context, networkID, structName, structID, step_params['filters'], step_params['assert'])

    safe(impl)


def assertForFilters(context, networkID, structName, structID, filters, assertItem):
    filterDto = requestToFilterDTO(filters)
    structInfo = readStructInfo(networkID, structName)

    request = FindObjectRequest(
        networkID=networkID,
        structID=structID,
        structInfo=structInfo,
        filters=[filterDto],
        paginator=PaginatorDTO(
            page=0,
            size=10,
            fields=[],
            orders=[]
        )
    )

    debugProto('request', request)
    result = context.mongodbServiceStub.FindObjectByFilter(request)
    debugProto('response', result)

    assertion = flatten_json(assertItem, '.')
    for assertKey, assertValue in assertion.items():
        # extract value from StringValue
        objValue = deepgetattr(result, assertKey)
        assertEq(objValue, assertValue)


@when('в networkID "{networkID:d}" удаляем объект в структуре "{structName}" с id="{id}"')
def step_impl(context, networkID, structName, id):
    def impl():
        structID = readFromCache(structCacheKey(networkID, structName, 'id'))
        request = BasicScenarioObjDTO(
            networkID=networkID,
            structID=structID,
            objectID=id
        )
        

        debugProto('request', request)
        result = context.mongodbServiceStub.Remove(request)
        debugProto('response', result)

        assertEq(result.value, True)
        
    safe(impl)


@when('в networkID "{networkID:d}" строим аггрегацию по структуре "{structName}"')
def step_impl(context, networkID, structName):
    def impl():
        structID = readFromCache(structCacheKey(networkID, structName, 'id'))
        structInfo = readStructInfo(networkID, structName)
        step_params = json.loads(context.text)

        request_params = step_params['request']
        filters = request_params['filters']
        filterDto = requestToFilterDTO(filters)

        aggregation = request_params['aggregation']
        aggregationField = request_params['aggregationField']

        request = SimpleAggregateRequest(
            networkID=networkID,
            structID=structID,
            filters=[filterDto],
            structInfo=structInfo,
            aggregation=aggregation,
            aggregationField=aggregationField
            )
        
        debugProto('request', request)
        result = context.mongodbServiceStub.SimpleAggregate(request)
        debugProto('response', result)

        assertion = flatten_json(step_params['assert'], '.')
        for assertKey, assertValue in assertion.items():
            # extract value from StringValue
            objValue = deepgetattr(result, assertKey)
            assertEq(objValue, assertValue)

    safe(impl)



# without params and expressions, ds has no js engine
# {
#     "name": "exclude",
#     "typeVariable" : "string",
#     "defValue" : "Петр",
#     "id" : "100"
# }
@when('в networkID "{networkID:d}" создаем отчет по структуре "{structName}"')
def step_impl(context, networkID, structName):
    def impl():
        structID = readFromCache(structCacheKey(networkID, structName, 'id'))
        step_params = json.loads(context.text)
        settings_param = step_params['request']['settings']
        settingsDto = settingsToDto(structID, settings_param)
        sysName = str(uuid.uuid4())
        request = GenerateReportStructureRequest(
            networkID=networkID,
            structID=structID,
            name=settings_param['name'],
            sysName=sysName,
            userID=0,
            folderID=0,
            settings = settingsDto
        )

        debugProto('request - generate metadata', request)
        result = context.metadataServiceStub.GenerateReportStructure(request)
        debugProto('response - generate metadata', result)

        buildReportRequest = BuildReportRequest(
            networkID=networkID,
            structID=structID,
            settings=result
        )
        debugProto('request - build report', buildReportRequest)
        buildResult = context.mongodbServiceStub.Report(buildReportRequest)
        debugProto('response - build report', buildResult)

        targetStructureID = result.resultStructID
        debug('target report structure id', targetStructureID)

        search_assertion = step_params['assert']
        
        # TODO targetStructSysName(hbase only)
        assertForFilters(context, networkID, 'TODO', targetStructureID,
                         search_assertion['filters'], search_assertion['assert'])

        # TODO extrat resultStructID from result, or just use for report run

    safe(impl)


@then('в networkID "{networkID:d}" потоково собираем объекты из структуры "{structName}"')
def step_impl(context, networkID, structName):
    def impl():
        structID = readFromCache(structCacheKey(networkID, structName, 'id'))
        step_params = json.loads(context.text)

        request = NetworkIDWithStructIDRequest(
            networkID=networkID,
            structID=structID
        )
        debugProto('request', request)
        result = context.mongodbServiceStub.ProcessObjects(request)

        resultItems = list()
        for item in result:
            resultItems.append(item)

        debug('response items', resultItems)
        assertEq(step_params['size'], len(resultItems))

    safe(impl)


@then('в networkID "{networkID:d}" потоково собираем поля "{fieldNames}" из структуры "{structName}"')
def step_impl(context, networkID, fieldNames, structName):
    def impl():
        structID = readFromCache(structCacheKey(networkID, structName, 'id'))
        structInfo = readStructInfo(networkID, structName)
        step_params = json.loads(context.text)
        fields = map(lambda x: x.strip(), fieldNames.split(","))

        request = ProcessObjectRequest(
            networkID=networkID,
            structID=structID,
            fieldNames=fields,
            structInfo=structInfo
        )
        debugProto('request', request)
        result = context.mongodbServiceStub.ProcessObjectsWithFields(request)

        resultItems = list()
        for item in result:
            resultItems.append(item)

        debug('response items', resultItems)
        assertEq(step_params['size'], len(resultItems))

        assertion = flatten_json(step_params['assert'], '.')
        for assertKey, assertValue in assertion.items():
            # extract value from StringValue
            objValue = deepgetattr(resultItems, assertKey)
            assertEq(objValue, assertValue)

    safe(impl)


def templatePattern(pattern, idx):
    result = {}
    if isinstance(pattern, dict):
        for patternKey, patternValue in pattern.items():
            if isinstance(patternValue, dict):
                result[patternKey] = templatePattern(patternValue, idx)
            else:
                if '%' in patternValue:
                    result[patternKey] = doTemplate(patternValue, idx)
                else:
                    result[patternKey] = patternValue
    else:
        if '%' in pattern:
            return doTemplate(pattern, idx)
        else:
            return pattern

    return result

def doTemplate(pattern, idx):
    if pattern.startswith('int:'):
        actual = pattern[4:]
        templated = actual % idx
        return int(templated)
    else:
        return pattern % idx

def reportParamsToDto(params):
    return ReportSettingsDTO.Parameter(
        name=params['name'],
        typeVariable=params['typeVariable'],
        defValue=params['defValue'], 
        id=params['id']
    )

def reportFieldToDto(field):
    return ReportSettingsDTO.Field(
        field=field['field'],
        id=field['id']
    )


def reportAggregationsToDto(aggr):
    return ReportSettingsDTO.Aggregation(
        field=aggr['field'],
        fn=aggr['fn'],
        id=aggr['id'],
        resultFieldName=aggr['resultFieldName']
    )


def reportGroupToDto(group):
    fields = list(map(reportFieldToDto, group['fields']))
    aggregations = list(map(reportAggregationsToDto, group['aggregations']))
    return ReportSettingsDTO.Group(
        fields=fields,
        aggregations=aggregations,
        id=group['id']
    )

def reportAggregationFiltersToDto(filter):
    return ReportSettingsDTO.AggregationFilter(
        aggregationId=filter['aggregationId'],
        exp=filter['exp'],
        value=filter['value'],
        isExp=filter['isExp']
    )

def settingsToDto(structID, settings):
    parameters = list(map(reportParamsToDto, settings['parameters']))
    fields = list(map(reportFieldToDto, settings['fields']))
    groups = list(map(reportGroupToDto, settings['groups']))
    postFilters = list(map(reportAggregationFiltersToDto, settings['postFilters']))
    
    preFilters = settings['preFilters']
    preFiltersJsonRaw = list(map(json.dumps, preFilters))

    dto = ReportSettingsDTO(
        name=settings['name'],
        structID=structID,
        resultStructID=0,
        preFiltersType=settings['preFiltersType'],
        postFiltersType=settings['postFiltersType'],
        parameters=parameters,
        fields=fields,
        groups=groups,
        preFiltersJsonRaw=preFiltersJsonRaw,
        postFilters=postFilters
    )
    return dto


def structCacheKey(networkID, sysName, field):
    result = '%s_%s_%s' % (networkID, sysName, field)
    return result


def dataToChangeFieldObjects(data):
    result = list(
        map(lambda kv: kvToExpressionResultDto(kv[0], kv[1]), data.items())
    )
    return result


def kvToExpressionResultDto(k,v):
    result = ExpressionResultDto(
        fieldName=k,
        dataValue=valueToFieldDataValue(v),
        expressionType=ExpressionResultType.Name(SET)
    )
    return result


def dataToFieldsValues(data):
    result = dict(
        map(lambda kv: (kv[0], valueToFieldDataValue(kv[1])), data.items()))
    response = FieldsValues(values = result)
    return response


def requestToFilterDTO(request):
    if 'op' in request:
        op = request['op']
        if 'innerFilters' in request:
            inner = list(map(requestToFilterDTO, request['innerFilters']))
            return FilterDTO(
                op=op,
                innerFilters=inner
            )
        else:
            return FilterDTO(
                op=op,
                field=request['field'],
                value=request['value']
            )
    else:
        return FilterDTO()



def valueToFieldDataValue(value):
    debug(value)
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


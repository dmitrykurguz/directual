# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: DatasourceRemoteService.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
import DTO_pb2 as DTO__pb2
import CommonRequestResponse_pb2 as CommonRequestResponse__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='DatasourceRemoteService.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x1d\x44\x61tasourceRemoteService.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\tDTO.proto\x1a\x1b\x43ommonRequestResponse.proto2\xe2\x11\n\x17\x44\x61tasourceRemoteService\x12\x38\n\x04Ping\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12R\n\rUpdateIndeces\x12\'.NetworkIDWithStructIDWithFieldsRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\x43\n\x08Truncate\x12\x1d.NetworkIDWithStructIDRequest\x1a\x16.google.protobuf.Empty\"\x00\x12U\n\x10RemoveFieldsData\x12\'.NetworkIDWithStructIDWithFieldsRequest\x1a\x16.google.protobuf.Empty\"\x00\x12G\n\x14NativeVersionSupport\x12\x11.NetworkIDRequest\x1a\x1a.google.protobuf.BoolValue\"\x00\x12L\n\x04Save\x12\'.ScenarioObjectDTOWrapperWithStructInfo\x1a\x19.ScenarioObjectDTOWrapper\"\x00\x12\\\n\tSaveBatch\x12\x35.NetworkIDWithScenarioObjectListRequestWithStructInfo\x1a\x16.ScenarioObjectListDTO\"\x00\x12K\n\tFindBySID\x12\".BasicScenarioObjDTOWithStructInfo\x1a\x18.ScenarioObjectOptionDTO\"\x00\x12K\n\tFindByOID\x12\".BasicScenarioObjDTOWithStructInfo\x1a\x18.ScenarioObjectOptionDTO\"\x00\x12U\n\x13\x46indByOIDWithFields\x12\".BasicScenarioObjWithFieldsRequest\x1a\x18.ScenarioObjectOptionDTO\"\x00\x12\x62\n\x0fSimpleFindByOID\x12\x33.NetworkIDWithStructIDWithObjectIDWithFieldsRequest\x1a\x18.ScenarioObjectOptionDTO\"\x00\x12=\n\x06\x46ields\x12\".BasicScenarioObjWithFieldsRequest\x1a\r.FieldsValues\"\x00\x12U\n\rFieldsPartial\x12\x33.NetworkIDWithStructIDWithObjectIDWithFieldsRequest\x1a\r.FieldsValues\"\x00\x12:\n\x08Versions\x12\x10.VersionsRequest\x1a\x1a.VersionInformationListDTO\"\x00\x12\x64\n\x13SystemFieldVersions\x12/.BasicScenarioObjWithMaxVersionWithFieldRequest\x1a\x1a.VersionInformationListDTO\"\x00\x12;\n\x05\x45xist\x12\x14.BasicScenarioObjDTO\x1a\x1a.google.protobuf.BoolValue\"\x00\x12\x36\n\x06\x45xists\x12\x0e.ExistsRequest\x1a\x1a.google.protobuf.BoolValue\"\x00\x12\x37\n\x06Report\x12\x13.BuildReportRequest\x1a\x16.google.protobuf.Empty\"\x00\x12<\n\x06Remove\x12\x14.BasicScenarioObjDTO\x1a\x1a.google.protobuf.BoolValue\"\x00\x12\x35\n\x04List\x12\x12.StructListRequest\x1a\x17.ScenarioObjectPagedDTO\"\x00\x12J\n\tTableSize\x12\x1d.NetworkIDWithStructIDRequest\x1a\x1c.google.protobuf.UInt64Value\"\x00\x12:\n\x0bLastObjects\x12\x11.NetworkIDRequest\x1a\x16.ScenarioObjectListDTO\"\x00\x12G\n\x11\x43hangeFieldObject\x12\x16.FieldsWithDataRequest\x1a\x18.ScenarioObjectOptionDTO\"\x00\x12\x45\n\x12NativeIndexSupport\x12\x11.NetworkIDRequest\x1a\x1a.google.protobuf.BoolValue\"\x00\x12K\n\x18NativeAggregationSupport\x12\x11.NetworkIDRequest\x1a\x1a.google.protobuf.BoolValue\"\x00\x12?\n\x0bHealthcheck\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12\x43\n\x12\x46indObjectByFilter\x12\x12.FindObjectRequest\x1a\x17.ScenarioObjectPagedDTO\"\x00\x12\x43\n\x0eProcessObjects\x12\x1d.NetworkIDWithStructIDRequest\x1a\x0e.ObjectInfoDTO\"\x00\x30\x01\x12K\n\x18ProcessObjectsWithFields\x12\x15.ProcessObjectRequest\x1a\x14.ObjectWithFieldsDTO\"\x00\x30\x01\x12<\n\x0b\x42\x61tchFields\x12\x13.BatchFieldsRequest\x1a\x14.ObjectWithFieldsDTO\"\x00\x30\x01\x12=\n\x0fSimpleAggregate\x12\x17.SimpleAggregateRequest\x1a\x0f.FieldDataValue\"\x00\x42\x35\n com.directual.generated.servicesB\x0f\x44\x61taSourceProtoP\x01\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,DTO__pb2.DESCRIPTOR,CommonRequestResponse__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n com.directual.generated.servicesB\017DataSourceProtoP\001'))

_DATASOURCEREMOTESERVICE = _descriptor.ServiceDescriptor(
  name='DatasourceRemoteService',
  full_name='DatasourceRemoteService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=135,
  serialized_end=2409,
  methods=[
  _descriptor.MethodDescriptor(
    name='Ping',
    full_name='DatasourceRemoteService.Ping',
    index=0,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateIndeces',
    full_name='DatasourceRemoteService.UpdateIndeces',
    index=1,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._NETWORKIDWITHSTRUCTIDWITHFIELDSREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Truncate',
    full_name='DatasourceRemoteService.Truncate',
    index=2,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._NETWORKIDWITHSTRUCTIDREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='RemoveFieldsData',
    full_name='DatasourceRemoteService.RemoveFieldsData',
    index=3,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._NETWORKIDWITHSTRUCTIDWITHFIELDSREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='NativeVersionSupport',
    full_name='DatasourceRemoteService.NativeVersionSupport',
    index=4,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._NETWORKIDREQUEST,
    output_type=google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Save',
    full_name='DatasourceRemoteService.Save',
    index=5,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._SCENARIOOBJECTDTOWRAPPERWITHSTRUCTINFO,
    output_type=DTO__pb2._SCENARIOOBJECTDTOWRAPPER,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SaveBatch',
    full_name='DatasourceRemoteService.SaveBatch',
    index=6,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._NETWORKIDWITHSCENARIOOBJECTLISTREQUESTWITHSTRUCTINFO,
    output_type=DTO__pb2._SCENARIOOBJECTLISTDTO,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='FindBySID',
    full_name='DatasourceRemoteService.FindBySID',
    index=7,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._BASICSCENARIOOBJDTOWITHSTRUCTINFO,
    output_type=DTO__pb2._SCENARIOOBJECTOPTIONDTO,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='FindByOID',
    full_name='DatasourceRemoteService.FindByOID',
    index=8,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._BASICSCENARIOOBJDTOWITHSTRUCTINFO,
    output_type=DTO__pb2._SCENARIOOBJECTOPTIONDTO,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='FindByOIDWithFields',
    full_name='DatasourceRemoteService.FindByOIDWithFields',
    index=9,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._BASICSCENARIOOBJWITHFIELDSREQUEST,
    output_type=DTO__pb2._SCENARIOOBJECTOPTIONDTO,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SimpleFindByOID',
    full_name='DatasourceRemoteService.SimpleFindByOID',
    index=10,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._NETWORKIDWITHSTRUCTIDWITHOBJECTIDWITHFIELDSREQUEST,
    output_type=DTO__pb2._SCENARIOOBJECTOPTIONDTO,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Fields',
    full_name='DatasourceRemoteService.Fields',
    index=11,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._BASICSCENARIOOBJWITHFIELDSREQUEST,
    output_type=DTO__pb2._FIELDSVALUES,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='FieldsPartial',
    full_name='DatasourceRemoteService.FieldsPartial',
    index=12,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._NETWORKIDWITHSTRUCTIDWITHOBJECTIDWITHFIELDSREQUEST,
    output_type=DTO__pb2._FIELDSVALUES,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Versions',
    full_name='DatasourceRemoteService.Versions',
    index=13,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._VERSIONSREQUEST,
    output_type=DTO__pb2._VERSIONINFORMATIONLISTDTO,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SystemFieldVersions',
    full_name='DatasourceRemoteService.SystemFieldVersions',
    index=14,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._BASICSCENARIOOBJWITHMAXVERSIONWITHFIELDREQUEST,
    output_type=DTO__pb2._VERSIONINFORMATIONLISTDTO,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Exist',
    full_name='DatasourceRemoteService.Exist',
    index=15,
    containing_service=None,
    input_type=DTO__pb2._BASICSCENARIOOBJDTO,
    output_type=google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Exists',
    full_name='DatasourceRemoteService.Exists',
    index=16,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._EXISTSREQUEST,
    output_type=google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Report',
    full_name='DatasourceRemoteService.Report',
    index=17,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._BUILDREPORTREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Remove',
    full_name='DatasourceRemoteService.Remove',
    index=18,
    containing_service=None,
    input_type=DTO__pb2._BASICSCENARIOOBJDTO,
    output_type=google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='List',
    full_name='DatasourceRemoteService.List',
    index=19,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._STRUCTLISTREQUEST,
    output_type=DTO__pb2._SCENARIOOBJECTPAGEDDTO,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='TableSize',
    full_name='DatasourceRemoteService.TableSize',
    index=20,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._NETWORKIDWITHSTRUCTIDREQUEST,
    output_type=google_dot_protobuf_dot_wrappers__pb2._UINT64VALUE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='LastObjects',
    full_name='DatasourceRemoteService.LastObjects',
    index=21,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._NETWORKIDREQUEST,
    output_type=DTO__pb2._SCENARIOOBJECTLISTDTO,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ChangeFieldObject',
    full_name='DatasourceRemoteService.ChangeFieldObject',
    index=22,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._FIELDSWITHDATAREQUEST,
    output_type=DTO__pb2._SCENARIOOBJECTOPTIONDTO,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='NativeIndexSupport',
    full_name='DatasourceRemoteService.NativeIndexSupport',
    index=23,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._NETWORKIDREQUEST,
    output_type=google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='NativeAggregationSupport',
    full_name='DatasourceRemoteService.NativeAggregationSupport',
    index=24,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._NETWORKIDREQUEST,
    output_type=google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Healthcheck',
    full_name='DatasourceRemoteService.Healthcheck',
    index=25,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='FindObjectByFilter',
    full_name='DatasourceRemoteService.FindObjectByFilter',
    index=26,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._FINDOBJECTREQUEST,
    output_type=DTO__pb2._SCENARIOOBJECTPAGEDDTO,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ProcessObjects',
    full_name='DatasourceRemoteService.ProcessObjects',
    index=27,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._NETWORKIDWITHSTRUCTIDREQUEST,
    output_type=DTO__pb2._OBJECTINFODTO,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ProcessObjectsWithFields',
    full_name='DatasourceRemoteService.ProcessObjectsWithFields',
    index=28,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._PROCESSOBJECTREQUEST,
    output_type=DTO__pb2._OBJECTWITHFIELDSDTO,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='BatchFields',
    full_name='DatasourceRemoteService.BatchFields',
    index=29,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._BATCHFIELDSREQUEST,
    output_type=DTO__pb2._OBJECTWITHFIELDSDTO,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SimpleAggregate',
    full_name='DatasourceRemoteService.SimpleAggregate',
    index=30,
    containing_service=None,
    input_type=CommonRequestResponse__pb2._SIMPLEAGGREGATEREQUEST,
    output_type=DTO__pb2._FIELDDATAVALUE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_DATASOURCEREMOTESERVICE)

DESCRIPTOR.services_by_name['DatasourceRemoteService'] = _DATASOURCEREMOTESERVICE

# @@protoc_insertion_point(module_scope)

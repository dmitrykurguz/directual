import time
import sys
import os
import pickle
import requests
import json
from flatten_json import flatten_json
from behave import given, when, then
from step_utils  import readCookieFromCache, appAddress, paramFromConfig, debug, logError


@then('объект структуры "{struct_name}" с id "{object_id}" имеет "{versions_count}" версии')
def step_impl(context, struct_name, object_id, versions_count):
  try:
    response = getVersions(context, struct_name, object_id)
    assert 'result' in response

    history = response['result']['history']
    assert len(history) == versions_count
  except AssertionError as ex:
    raise ex
  except Exception:
    logError()
    assert False


@then('версия "{struct_name}" с id "{object_id}" с индексом "{version_index}" точно соответствует')
def step_impl(context, struct_name, object_id, version_index):
  version = getVersionByIndex(context, struct_name, object_id, version_index)
  data = version['result']['container']
  real_fields = dict((key, value) for key, value in data.items() if not key.startswith('$'))
  assertion = json.loads(context.text)

  debug('check for data %s equals %s' % (json.dumps(data), assertion))
  
  assert assertion == real_fields


#FIXME copypaste here
def handleResponse(r):
  debug('response status: %s \n response text: \n %s' % (r.status_code, r.text))
  r.raise_for_status()    


def getVersions(context, struct_name, object_id, version = 0):
  app_id = paramFromConfig(context, 'app_id')
  app_secret = paramFromConfig(context, 'app_secret')
  debug('use app_id %s and app_secret %s' % (app_id, app_secret))

  #http://localhost:8081/good/api/v3/object/data/4283/?sessionid=34212c47-86b0-4671-943b-9b5f7920e15d
  #{"sessionid":"34212c47-86b0-4671-943b-9b5f7920e15d","history":true,"version":0,"structID":"test","objectID":"1","showLinkName":true}

  uri = '%s/good/api/v3/object/data/0/?appID=%s&appSecret=%s' % (appAddress(context), app_id, app_secret)

  # body = context.text
  body = '{"history": true, "version": %s, "structID": "%s", "objectID": "%s", "showLinkName": true}' % (
      version, struct_name, object_id)

  debug('call: %s' % uri, body)
  res = requests.post(uri, data=body)
  handleResponse(res)

  # TODO
  response = json.loads(res.text)
  return response


def getVersionByIndex(context, struct_name, object_id, version_index):
  versions = getVersions(context, struct_name, object_id)
  history = versions['result']['history']
  timestamp = list(reversed(history))[version_index]
  debug('version for index %s is %s' % (version_index, timestamp))

  specific_version = getVersions(context, struct_name, object_id, timestamp)
  debug('read version: %s' % json.dumps(specific_version))
  return specific_version

  # TODO 


#https://directual.com/good/api/v3/object/data/2595/?sessionid=50a7243f-db95-4763-83ab-c7f46e13e6b2
#{"sessionid":"50a7243f-db95-4763-83ab-c7f46e13e6b2","history":true,"version":1508151113774,"structID":"auctions","objectID":"NEW-PIM-2017-10-16-1.0"}

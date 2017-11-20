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
    app_id = paramFromConfig(context, 'app_id')
    app_secret = paramFromConfig(context, 'app_secret')
    debug('use app_id %s and app_secret %s' % (app_id, app_secret))

    #http://localhost:8081/good/api/v3/object/data/4283/?sessionid=34212c47-86b0-4671-943b-9b5f7920e15d
    #{"sessionid":"34212c47-86b0-4671-943b-9b5f7920e15d","history":true,"version":0,"structID":"test","objectID":"1","showLinkName":true}

    uri = '%s/good/api/v3/object/data/0/?appID=%s&appSecret=%s' % (appAddress(context), app_id, app_secret)

    # body = context.text
    body = '{"history": true, "version": 0, "structID": "%s", "objectID": "%s", "showLinkName": true}' % (struct_name, object_id)

    debug('call: %s' % uri, body)
    res = requests.post(uri, data=body)
    handleResponse(res)

    # TODO
    response = json.loads(res.text)
    assert 'result' in response

    history = response['result']['history']
    assert len(history) == 2
    
    assert False
  except AssertionError as ex:
    raise ex
  except Exception:
    logError()
    assert False


#FIXME copypaste here
def handleResponse(r):
  debug('response status: %s \n response text: \n %s' % (r.status_code, r.text))
  r.raise_for_status()    

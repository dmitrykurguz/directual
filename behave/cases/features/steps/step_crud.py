import time
import sys
import os
import pickle
import requests
import json
from flatten_json import flatten_json
from behave import given, when, then
from step_utils  import readCookieFromCache, appAddress, paramFromConfig, debug, logError


@given('отправляем авторизованный запрос на "{path}"')
def step_impl(context, path):
  try:
    sessionid = readCookieFromCache("sessionid")
    assert sessionid is not None
    
    uri = '%s%s?%s=%s' % (appAddress(context), path, 'sessionid', sessionid['value'])
    debug('request %s with sessionId' % uri)
    
    r = requests.post(uri, data=context.text)
    handleResponse(r)
  except Exception:
    logError()
    assert False
  
@when('сохраняем объект структуры "{struct_name}"')
def step_impl(context, struct_name):
  try:
    app_id = paramFromConfig(context, 'app_id')
    app_secret = paramFromConfig(context, 'app_secret')
    debug('use app_id %s and app_secret %s' % (app_id, app_secret))

    uri = '%s/good/api/v3/struct/%s/?appID=%s&appSecret=%s' % (appAddress(context), struct_name, app_id, app_secret)
    debug('call: %s' % uri)
    res = requests.post(uri, data=context.text)
    handleResponse(res)
    result = json.loads(res.text)
    assert 'msg' not in result
  except Exception:
    logError()
    assert False
  

@given('присутствует объект структуры "{struct_name}" с id "{struct_id}"')
@when('присутствует объект структуры "{struct_name}" с id "{struct_id}"')
@then('присутствует объект структуры "{struct_name}" с id "{struct_id}"')
def step_impl(context, struct_name, struct_id):
  try:
    time.sleep(5) # FIXME remove it !
    app_id = paramFromConfig(context, 'app_id')
    app_secret = paramFromConfig(context, 'app_secret')
    debug('use app_id %s and app_secret %s' % (app_id, app_secret))

    body = '{"filters":[{"operator":"AND","field":"id","value":"%s","exp":"="}],"fetch":"","fields":"","pageSize":10,"page":0,"ref":"","allObjects":true,"orders":[]}' % id
    uri = '%s/good/api/v3/struct/%s/search/?appID=%s&appSecret=%s' % (appAddress(context), struct_name, app_id, app_secret)

    debug('call: %s' % uri)
    res = requests.post(uri, data=body)
    debug(res.text)
    # handleResponse(res)

    response = json.loads(res.text)
    # debug(response) # TODO try to uncoment, it's object, check alive test!

    assert 'result' in response
    results = response['result']
    assert 'list' in results
    assert len(results['list']) == 1


  except Exception, e:
    if isinstance(e, AssertionError):
      raise e
    logError()
    assert False


# @given('присутствует объект структуры "{struct_name}" с id "{id}"')
# @when( 'присутствует объект структуры "{struct_name}" с id "{id}"')
# @then('присутствует объект структуры "{struct_name}" с id "{id}"')
# def step_impl(context, struct_name, id):
#   try:
#     app_id = paramFromConfig(context, 'app_id')
#     app_secret = paramFromConfig(context, 'app_secret')
#     debug('use app_id %s and app_secret %s' % (app_id, app_secret))

#     body = '{"filters":[{"operator":"AND","field":"id","value":"%s","exp":"="}],"fetch":"","fields":"","pageSize":10,"page":0,"ref":"","allObjects":true,"orders":[]}' % id
#     uri = '%s/good/api/v3/struct/%s/search/?appID=%s&appSecret=%s' % (appAddress(context), struct_name, app_id, app_secret)

#     debug('call: %s' % uri)
#     r = requests.post(uri, data=body)
#     handleResponse(r)

#     response = json.loads(r.text)
#     debug(response)

#     assert 'result' in response
#     results = response['result']
#     assert 'list' in results
#     assert len(results['list']) == 1
#   except Exception:
#     logError()
#     assert False



@then('объект структуры "{struct_name}" имеет поля')
def step_impl(context, struct_name):
  try:
    app_id = paramFromConfig(context, 'app_id')
    app_secret = paramFromConfig(context, 'app_secret')
    
    step_params = json.loads(context.text)
    filters = step_params['filter']
    assertion = flatten_json(step_params['assert'])

    uri = '%s/good/api/v3/struct/%s/search/?appID=%s&appSecret=%s' % (appAddress(context), struct_name, app_id, app_secret)  
    debug('looking %s with filters: %s' % (struct_name, filters))
    debug('call: %s' % uri)
    r = requests.post(uri, data=json.dumps(filters))
    handleResponse(r)

    result = json.loads(r.text)
    resultList = result['result']['list']
    assert len(resultList) == 1
    item = resultList[0]['obj']
    debug('item = %s' % item)
    debug(assertion)

    flattenItem = flatten_json(item)
    for assertKey, assertValue in assertion.items():
      assert flattenItem[assertKey] == assertValue
  except Exception:
    logError()
    assert False


def handleResponse(r):
  debug('response status: %s \n response text: \n %s' % (r.status_code, r.text))
  r.raise_for_status()





